from flask import Blueprint, request, jsonify

from visor.organization.org import create_org, select_org

org_app = Blueprint("org_apis", __name__)

@org_app.get("/")
def root():
    return {"message": "Hello from org!"}


@org_app.get("/healthz")
def health_check():
    return {"response": "ok"}



# admin apis
# create org
@org_app.post("/create")
def create_org_flow():
    req = request.json

    res = create_org(req.get("org_name"))

    return jsonify(res)


@org_app.route("/<org_id>", methods=["GET"])
def select_org_flow(org_id):
    
    res = select_org(org_id)
    return jsonify(res.model_dump())


# delete org



# remove people
# update people