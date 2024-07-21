import uuid
from flask import Blueprint, request, jsonify

from visor.utils import init_logger
from visor.types import Deployment, DeploymentStatus, Cluster
from visor.resource_manager.deployment import create_deployment, select_deployment, select_all_deployment
from visor.resource_manager.cluster import create_cluster, select_cluster, select_all_cluster, clear_cluster_schedule_queue


logger=init_logger(__name__)
res_man_app = Blueprint("resource_manage_apis", __name__)


@res_man_app.get("/")
def root():
    return {"message": "Hello from resource manager!"}


@res_man_app.get("/healthz")
def health_check():
    return {"response": "ok"}

@res_man_app.post("/create/cluster")
def create_cluster_flow():
    """
        {
            cluster : {
                "requested_mem": 1.0,
                "requested_cpu": 1.0,
            },
            org_id : ""
        }
    """
    req = request.json
    c = req.get("cluster")

    cluster = Cluster(org_id=req.get("org_id"), cluster_id=uuid.uuid4(), assigned_mem=c.get("requested_mem"), assigned_cpu=c.get("requested_cpu"), available_mem=c.get("requested_mem"), available_cpu=c.get("requested_cpu") )

    try:
        create_cluster(cluster)
        return jsonify(cluster.model_dump())
    except Exception as err:
        logger.exception("error occured while createing deployment")
        return jsonify(
            {
                "message": "Failed to create cluster. Please try again"
            }
        )

@res_man_app.get("/cluster/<org_id>")
def list_cluster(org_id):
    try:
        res = select_all_cluster(org_id)
        return jsonify(res.model_dump())
    except Exception as err:
        logger.exception("error occured while createing deployment")
        return jsonify(
            {
                "message": "Failed to list clusters. Please try again"
            }
        )

@res_man_app.get("/cluster/<org_id>/<cluster_id>")
def select_cluster_flow(org_id, cluster_id):
    try:
        res = select_cluster(org_id, cluster_id)
        return jsonify(res.model_dump())
    except Exception as err:
        logger.exception("error occured while createing deployment")
        return jsonify(
            {
                "message": "Failed to get clusters. Please try again"
            }
        )



@res_man_app.post("/schedule/deployment")
def schedule_deployment():
    """
        {
            deployment : {
                "yaml": {}
                "priority": [1-10]
                "requested_mem": 1.0,
                "requested_cpu": 1.0,
            },
            org_id : ""
            cluster_id: ""
        }
    """
    req = request.json
    dep = req.get("deployment")
    deploy = Deployment(org_id=req.get("org_id"), cluster_id=req.get("cluster_id"),deployment_id=uuid.uuid4() ,status=DeploymentStatus.PENDING, **dep)
    
    try:
        create_deployment(deploy)
        return jsonify(deploy.model_dump())
    except Exception as err:
        logger.exception("error occured while createing deployment")
        return jsonify(
            {
                "message": "Failed to create deployment. Please try again"
            }
        )
    

@res_man_app.get("/deployment/<org_id>/<cluster_id>")
def list_deployments(org_id, cluster_id):
    try:
        res = select_all_deployment(org_id, cluster_id)
        return jsonify(res.model_dump())
    except Exception as err:
        logger.exception("error occured while createing deployment")
        return jsonify(
            {
                "message": "Failed to list deployments. Please try again"
            }
        )


@res_man_app.get("/deployment/<org_id>/<cluster_id>/<deployment_id>")
def select_deployments(org_id, cluster_id, deployment_id):
    try:
        res = select_deployment(org_id, cluster_id, deployment_id)
        return jsonify(res.model_dump())
    except Exception as err:
        logger.exception("error occured while createing deployment")
        return jsonify(
            {
                "message": "Failed to get deployments. Please try again"
            }
        )


@res_man_app.delete("/queue/<org_id>/<cluster_id>")
def clear_queue(org_id, cluster_id):
    try:
        clear_cluster_schedule_queue(org_id, cluster_id)
        return jsonify({
            "message": "queue cleared"
        })
    except Exception as err:
        logger.exception("error occured while clearing queue")
        return jsonify(
            {
                "message": "Failed to clear queue. Please try again"
            }
        )