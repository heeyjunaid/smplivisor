


# org
CREATE_ORG_QUERY = "INSERT INTO organization (org_name, org_created_at, invite_id, invite_id_created) VALUES (%s, %s, %s, %s)"
DELETE_ORG_QUERY = "DELETE FROM organization where org_id=%s"
UPDATE_ORG_INVITE_ID_QUERY = "UPDATE "
SELECT_ORG_QUERY = "SELECT org_id, org_name, org_created_at, invite_id, invite_id_created FROM organization where org_id=%s" 

# cluster
CREATE_CLUSTER_QUERY = "INSERT INTO cluster (org_id, cluster_id, assigned_mem, assigned_cpu, available_mem, available_cpu) VALUES (%s, %s, %s, %s, %s, %s)"
SELECT_ALL_CLUSTER_QUERY = "SELECT * FROM cluster WHERE org_id = %s"
SELECT_CLUSTER_QUERY = "SELECT * FROM cluster WHERE org_id = %s AND cluster_id = %s"
UPDATE_CLUSTER_AVAILABLE_RESOURCE_QUERY = "UPDATE cluster SET available_mem = %s, available_cpu=%s WHERE org_id = %s AND cluster_id = %s"

# deployment
CREATE_DEPLOYMENT_QUERY = "INSERT INTO deployment (org_id, cluster_id, deployment_id, status, priority, requested_mem, requested_cpu) VALUES (%s, %s, %s, %s, %s, %s, %s)"
UPDATE_DEPLOYMENT_PRIORITY_QUERY = "UPDATE deployment SET priority = %s WHERE org_id = %s AND cluster_id = %s AND deployment_id = %s"
UPDATE_DEPLOYMENT_STATUS_QUERY = "UPDATE deployment SET status = %s WHERE org_id = %s AND cluster_id = %s AND deployment_id = %s"
SELECT_PENDING_DEPLOYMENT_QUERY = "SELECT * FROM deployment WHERE org_id = %s AND cluster_id = %s AND status = 'PENDING'"
SELECT_ALL_DEPLOYMENT_QUERY = "SELECT * FROM deployment WHERE org_id = %s AND cluster_id = %s"
SELECT_DEPLOYMENT_QUERY = "SELECT * FROM deployment WHERE org_id = %s AND cluster_id = %s AND deployment_id = %s"
