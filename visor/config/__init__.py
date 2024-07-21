import os
from visor.utils import init_logger

logger = init_logger(__name__)
 
def safeGetWithException(key:str):
    value = os.environ.get(key)

    if value is None:
        raise ValueError(f"ENV NOT FOUND for key: {key}") 
    return value

def safeGetWithDefault(key:str, default:str, ignore_warning=True):
    value = os.environ.get(key)
    if value is None:
        if not ignore_warning:
            logger.warning(f"ENV NOT FOUND for key: {key}, using default value")
        return default
    else:
        return value
    


# Database connection details
DB_HOST = safeGetWithDefault('DB_HOST', "localhost") 
DB_PORT = safeGetWithDefault('DB_PORT', "5432")
DB_NAME = safeGetWithDefault('DB_NAME', "visordb")
DB_USER = safeGetWithDefault('DB_USER', "visor")
DB_PASSWORD = safeGetWithDefault('DB_PASSWORD', "visor")


# Redis config
REDIS_HOST = safeGetWithDefault('DB_HOST', "localhost") 
REDIS_PORT = safeGetWithDefault('DB_HOST', "6379")

REDIS_CLUSTER_PROCESS_MAPPING_KEY =  safeGetWithDefault('REDIS_CLUSTER_PROCESS_MAPPING_KEY', "CLUSTER_PROCESS")
REDIS_HIGH_PRIORITY_QUEUE_KEY_BASE = safeGetWithDefault("REDIS_HIGH_PRIORITY_QUEUE_KEY_BASE", "HIGH_PRIORITY_QUEUE")
REDIS_LOW_PRIORITY_QUEUE_KEY_BASE = safeGetWithDefault("REDIS_LOW_PRIORITY_QUEUE_KEY_BASE", "LOW_PRIORITY_QUEUE")

SCHEDULER_QUEUE_AGING_THRESHOLD = int(safeGetWithDefault('SCHEDULER_QUEUE_AGING_THRESHOLD', 5)) 
