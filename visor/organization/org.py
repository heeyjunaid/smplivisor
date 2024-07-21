import uuid
from datetime import datetime


from visor.types import Organization
import visor.db.queries as db_query
from visor.db import DB_CONN, run_query, fetch_one


def create_org(org_name:str):
    if org_name is None:
        return

    created_at = datetime.now()
    invite_code = uuid.uuid4()  # make it 6 digit random number
    run_query(db_query.CREATE_ORG_QUERY, (org_name, created_at, str(invite_code), created_at))
    # TODO: get org id
    return Organization(org_name=org_name, created_at=created_at, invite_code=invite_code)

def select_org(ord_id:str):
    org = fetch_one(db_query.SELECT_ORG_QUERY, (ord_id, ))
    
    o = {
        "org_name":org[1], "org_id":org[0], "created_at":org[2], "invite_code":str(org[3]), "invite_code_created":org[4]
    }
    
    
    return Organization(**o)

def delete_org(ord_id:str):
    pass

def validate_org_invite_id(ord_id:str, in_code:str):
    org = select_org(ord_id)

    if org.invite_code != in_code:
        return False
    
    # TODO: Add time based check
    return True
    
    

