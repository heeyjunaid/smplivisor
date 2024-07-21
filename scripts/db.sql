create database visordb;
create user visor with password 'visor';
grant all on DATABASE visordb to visor;

\c visordb;

set Schema 'public';

CREATE TABLE organization (
    org_id SERIAL NOT NULL,
    org_name character varying(255) NOT NULL,
    org_created_at timestamp without time zone,
    invite_id uuid NOT NULL,
    invite_id_created timestamp without time zone, 
    PRIMARY KEY (org_id)
);

CREATE TYPE user_role as ENUM ('SUPER_ADMIN','ADMIN','DEVELOPER', 'VIEWER');

CREATE TABLE rbac (
    org_id INT NOT NULL,
    email character varying(255) NOT NULL,
    role user_role NOT NULL,
    password character varying(255) NOT NULL,
    PRIMARY KEY (org_id, email),
    FOREIGN KEY (org_id) REFERENCES organization (org_id)
);


CREATE TABLE cluster (
    org_id INT NOT NULL,
    cluster_id uuid NOT NULL,
    assigned_mem REAL NULL,
    assigned_cpu REAL NULL,
    available_mem REAL NULL,
    available_cpu REAL NULL,
    PRIMARY KEY (org_id, cluster_id),
    FOREIGN KEY (org_id) REFERENCES organization (org_id)
);

CREATE TYPE deployment_status as ENUM ('PENDING','RUNNING','FAILED');

CREATE TABLE deployment (
    org_id SERIAL NOT NULL,
    cluster_id uuid NOT NULL,
    deployment_id uuid NOT NULL,
    status deployment_status NOT NULL,
    priority INT NULL,
    requested_mem REAL NULL,
    requested_cpu REAL NULL, 
    PRIMARY KEY (org_id, cluster_id, deployment_id),
    FOREIGN KEY (org_id) REFERENCES organization (org_id)
);

ALTER TABLE organization OWNER TO visor;
ALTER TABLE rbac OWNER TO visor;
ALTER TABLE cluster OWNER TO visor;
ALTER TABLE deployment OWNER TO visor;

