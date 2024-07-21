from typing import List
from datetime import datetime
from pydantic import BaseModel
from enum import Enum
import uuid


class Organization(BaseModel):
    org_name : str
    org_id : int
    created_at : datetime
    invite_code : str
    invite_code_created : datetime


class UserRole(str, Enum):
    SUPER_ADMIN = 'SUPER_ADMIN'
    ADMIN = 'ADMIN'
    DEVELOPER = 'DEVELOPER'
    VIEWER = 'VIEWER'

class RBAC(BaseModel):
    org_id: int
    email: str
    role: UserRole
    password: str
        
class Cluster(BaseModel):
    org_id: int
    cluster_id: uuid.UUID
    assigned_mem: float
    available_mem: float
    assigned_cpu: float
    available_cpu: float

class ClusterList(BaseModel):
    clusters : List[Cluster]

class DeploymentStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    FAILED = "FAILED"

class Deployment(BaseModel):
    org_id: int
    cluster_id: uuid.UUID
    deployment_id: uuid.UUID
    status: DeploymentStatus
    priority: int
    requested_mem: float
    requested_cpu: float
    wait_time: int = 0  # Track the waiting time of the deployment

    def __lt__(self, other):
        # This ensures the heapq works as a max-heap based on priority
        return self.priority > other.priority

class DeploymentList(BaseModel):
    deployments : List[Deployment]


class RedisQueueStatus(Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    DONE = "DONE"