from typing import List

import time
import redis
import uuid
import threading

import visor.config as config
from visor.types import Deployment, RedisQueueStatus, Cluster, DeploymentStatus
from visor.db.redis import redis_client, create_redis_key, get_ids_from_key
import visor.db.queries as q
from visor.db import fetch_one, run_query
from visor.utils import init_logger


logger = init_logger(__name__)


def priority_based_scheduling(org_id:int, cluster_id:uuid.uuid4, redis_client : redis.StrictRedis, available_mem, available_cpu, aging_threshold):
    high_priority_queue_key = create_redis_key(org_id, cluster_id, config.REDIS_HIGH_PRIORITY_QUEUE_KEY_BASE)
    low_priority_queue_key = create_redis_key(org_id, cluster_id, config.REDIS_LOW_PRIORITY_QUEUE_KEY_BASE)

    while redis_client.zcard(high_priority_queue_key) > 0 or redis_client.llen(low_priority_queue_key) > 0:
        if redis_client.zcard(high_priority_queue_key) > 0:
            deployment_data = redis_client.zpopmax(high_priority_queue_key)[0][0]
        else:
            deployment_data = redis_client.lpop(low_priority_queue_key)

        deployment = Deployment(**deployment_data)
        
        if deployment.requested_mem <= available_mem and deployment.requested_cpu <= available_cpu:
            # updating deployment status in psql
            logger.info(f"deployment done: {deployment.org_id}::{deployment.cluster_id}::{deployment.deployment_id}")
            run_query(q.UPDATE_DEPLOYMENT_STATUS_QUERY, (DeploymentStatus.RUNNING.value, deployment.org_id, str(deployment.cluster_id), str(deployment.deployment_id)))
            available_mem -= deployment.requested_mem
            available_cpu -= deployment.requested_cpu
        else:
            if deployment.priority > 1:
                deployment.priority -= 1  # Decrease priority for aging effect
                redis_client.zadd(high_priority_queue_key, {deployment.model_dump_json(): deployment.priority})
            else:
                deployment.wait_time += 1
                if deployment.wait_time > aging_threshold:
                    deployment.priority += 1  # Increase priority due to long wait
                redis_client.rpush(high_priority_queue_key, deployment.model_dump_json())
 
    logger.info(f"scheduling of queue {org_id}::{cluster_id} is done. updating avaialble resources")
    run_query(q.UPDATE_CLUSTER_AVAILABLE_RESOURCE_QUERY, (available_mem, available_cpu, org_id, str(cluster_id)))
    return True


def schedule_queue(queue_name):
    logger.info(f"scheduling queue: {queue_name}")
    org_id, cluster_id = get_ids_from_key(queue_name)

    res = fetch_one(q.SELECT_CLUSTER_QUERY, (org_id, str(cluster_id)))

    if res is None:
        logger.info(f"No cluster found with id {org_id}::{cluster_id}")
        return 

    o =  {
            "org_id": res[0],
            "cluster_id": res[1],
            "assigned_mem": res[2],
            "available_mem": res[3],
            "assigned_cpu": res[4],
            "available_cpu": res[5]
            }
    cluster = Cluster(**o)

    
    redis_client.hset(config.REDIS_CLUSTER_PROCESS_MAPPING_KEY, queue_name, RedisQueueStatus.RUNNING.value)
    thread = threading.Thread(target=priority_based_scheduling, args=( org_id, cluster_id, redis_client, cluster.assigned_mem, cluster.available_cpu, config.SCHEDULER_QUEUE_AGING_THRESHOLD))
    thread.daemon = True  # Make the thread a daemon thread
    thread.start()


def run_infinte():
    while True:
        run_once()
        # adding cooloff in infinte while loop
        time.sleep(10)

def run_once():
    queue_status = redis_client.hgetall(config.REDIS_CLUSTER_PROCESS_MAPPING_KEY)
    for queue_name, status in queue_status.items():
        if status == RedisQueueStatus.PENDING.value:
            schedule_queue(queue_name)