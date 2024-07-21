import redis

from visor.utils import init_logger

logger = init_logger(__name__)

def create_redis_client():
    try:
        return redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
    except Exception as err:
        raise Exception("Some error occured while connecting with redis")
    

redis_client = create_redis_client()


def create_redis_key(org_id, cluster_id, key_base:str):
    return f"{key_base}::{org_id}::{cluster_id}"

def get_ids_from_key(key):
    # assuming key is always created with some base name
    return key.split("::")[1:]