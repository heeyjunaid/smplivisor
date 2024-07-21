import uuid

from visor.types import Cluster, ClusterList
from visor.db import run_query, fetch_one, fetch_all
import visor.config as config
import visor.db.queries as q
from visor.db.redis import redis_client, create_redis_key
from visor.utils import init_logger

logger = init_logger(__name__)

def create_cluster(cluster:Cluster):
    run_query(q.CREATE_CLUSTER_QUERY, (cluster.org_id, str(cluster.cluster_id), cluster.assigned_mem, cluster.assigned_cpu, cluster.assigned_mem, cluster.assigned_cpu)) 
    return True

def form_cluster(res:tuple) -> Cluster:
    o =  {
            "org_id": res[0],
            "cluster_id": res[1],
            "assigned_mem": res[2],
            "available_mem": res[3],
            "assigned_cpu": res[4],
            "available_cpu": res[5]
            }
    return Cluster(**o)



def select_cluster(org_id:int, cluster_id:uuid.UUID) -> Cluster:
    res = fetch_one(q.SELECT_CLUSTER_QUERY, (org_id, str(cluster_id)))
    return form_cluster(res)


def select_all_cluster(ord_id:int) -> ClusterList:
    res = fetch_all(q.SELECT_ALL_CLUSTER_QUERY, (ord_id, ))

    cs = []
    for r in res:
        cs.append(form_cluster(r))

    return ClusterList(clusters=cs)


def clear_cluster_schedule_queue(org_id:str, cluster_id:uuid.UUID):
    hkey = create_redis_key(org_id, cluster_id, config.REDIS_HIGH_PRIORITY_QUEUE_KEY_BASE)
    lkey = create_redis_key(org_id, cluster_id, config.REDIS_LOW_PRIORITY_QUEUE_KEY_BASE)
    logger.info(f"deleting high priority queue - {hkey} ")
    redis_client.delete(hkey)
    logger.info(f"deleting low priority queue - {lkey} ")
    redis_client.delete(lkey)
    # creating lock
    redis_client.hdel(config.REDIS_CLUSTER_PROCESS_MAPPING_KEY, hkey)
    return True

