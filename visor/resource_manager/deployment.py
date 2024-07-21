import uuid

from visor.types import Deployment, RedisQueueStatus, DeploymentList
import visor.config as config
from visor.db.redis import redis_client, create_redis_key
import visor.db.queries as q
from visor.db import run_query, fetch_one, fetch_all


def create_deployment(deploy:Deployment):

    run_query(q.CREATE_DEPLOYMENT_QUERY, (deploy.org_id, str(deploy.cluster_id), str(deploy.deployment_id), deploy.status.value, deploy.priority, deploy.requested_cpu, deploy.requested_mem))

    rkey = create_redis_key(deploy.org_id, deploy.cluster_id, config.REDIS_HIGH_PRIORITY_QUEUE_KEY_BASE)
    redis_client.zadd(rkey, {deploy.model_dump_json():deploy.priority})

    # also update status in redis processing queue
    status = redis_client.hget(config.REDIS_CLUSTER_PROCESS_MAPPING_KEY, rkey)

    if status is None or status == RedisQueueStatus.DONE.value:
        redis_client.hset(config.REDIS_CLUSTER_PROCESS_MAPPING_KEY, rkey, RedisQueueStatus.PENDING.value)
    
    return True

def form_deployment(res:tuple) -> Deployment:
    o = {
            "org_id": res[0],
            "cluster_id": res[1],
            "deployment_id": res[2],
            "status": res[3],
            "priority": res[4],
            "requested_mem": res[5],
            "requested_cpu": res[6],
            "wait_time": res[7]
    }
    return Deployment(**o)



def select_deployment(org_id:int, cluster_id:uuid.uuid4, deployment_id:uuid.uuid4) -> Deployment:
    res = fetch_one(q.SELECT_DEPLOYMENT_QUERY, (org_id, str(cluster_id), str(deployment_id)))
    return form_deployment(res)

def select_all_deployment(org_id:int, cluster_id:uuid.uuid4):
    res = fetch_all(q.SELECT_ALL_DEPLOYMENT_QUERY, (org_id, str(cluster_id)))
    dps = []

    for r in res:
        dps.append(form_deployment(r))
    
    return DeploymentList(deployments=dps)