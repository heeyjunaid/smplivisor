from flask import Flask


from visor.app.organization import org_app
from visor.app.resource_manage import res_man_app

API_VERSION_PREFIX = "/api/v1"



app = Flask(__name__)
app.register_blueprint(org_app, url_prefix=API_VERSION_PREFIX+"/org")
app.register_blueprint(res_man_app, url_prefix=API_VERSION_PREFIX+"/manage")



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5213)