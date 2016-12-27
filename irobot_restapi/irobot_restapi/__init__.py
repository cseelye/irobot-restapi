#!/usr/bin/env python2.7
"""
REST API to control iRobot cleaning robots
"""

from flask import Flask, Blueprint
from flask_basicauth import BasicAuth
import importlib
import json
import os

from irobot_restapi.api import flask_api
from irobot_restapi.robot import ns


app = Flask(__name__)

api_blueprint = Blueprint("api", __name__, url_prefix="/api")
flask_api.init_app(api_blueprint)
app.register_blueprint(api_blueprint)

flask_api.add_namespace(ns)

#
# Setup the response headers
#
@app.after_request
def set_response_headers(response):
    """
    Rewrite the "server" header so we don't give away that information
    """
    # Flask/werkzeud does not allow us to remove the header entirely, so we write garbage into it instead
    response.headers["server"] = "asdf"
    return response


#
# Super basic and not terribly secure authentication
#
app.config["BASIC_AUTH_FORCE"] = True

class Authorizor(BasicAuth):

    def check_credentials(self, username, password):
        print "Authorization request for {}".format(username)
        userlist = []

        # First look for config file
        try:
            userlist = json.load(open(os.path.join(os.path.dirname(__file__), "userconfig.json")))
        except (ValueError):
            pass

        # Next look in ENV, handy for docker deployments.
        # Anything found here will overwrite config file values
        user = os.environ.get("IROBOT_USER")
        passwd = os.environ.get("IROBOT_PASS")
        if user and passwd:
            userlist[user] = passwd

        for user in userlist["users"]:
            if user["username"] == username and user["password"] == password:
                print "Valid credentials"
                return True
        print "Invalid credentials"
        return False

basic_auth = Authorizor(app)
