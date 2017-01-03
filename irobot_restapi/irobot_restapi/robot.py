#!/usr/bin/env python2.7

# System imports
from flask_restplus import abort, Resource
import json
import os
from pyirobot import Robot

# Internal imports
from irobot_restapi.api import flask_api

# Create my namespace
ns = flask_api.namespace('roomba', description="Control iRobot cleaning robots")

# Load my config file
config = json.load(open(os.path.join(os.path.dirname(__file__), "robotconfig.json")))

def GetRobot(robotName):
    """
    Helper function to find and instantiate a robot by name

    Returns:
        A ready to use Robot object (pyirobot.Robot)
    """
    roomba = None
    for robot_name, robot_config in config["robots"].iteritems():
        if robot_name == robotName:
            roomba = Robot(robot_config["ip"], robot_config["password"])
            break
    if not roomba:
        abort(500, "Could not find robot with name '{}'".format(robotName))
    return roomba

@ns.route("/")
class RoombaCollection(Resource):
    """
    List all of the known roombas
    """
    def get(self):
        result = {}
        for robot_name, robot_config in config["robots"].iteritems():
            result[robot_name] = robot_config["description"]

        return result

@ns.route("/<string:name>/start")
class RoombaStart(Resource):
    """
    Start a roomba
    """
    def get(self, name):
        GetRobot(name).StartCleaning()
        return {}

@ns.route("/<string:name>/pause")
class RoombaPause(Resource):
    """
    Pause a roomba
    """
    def get(self, name):
        GetRobot(name).PauseCleaning()
        return {}

@ns.route("/<string:name>/resume")
class RoombaResume(Resource):
    """
    Resume a roomba
    """
    def get(self, name):
        GetRobot(name).ResumeCleaning()
        return {}

@ns.route("/<string:name>/cancel")
class RoombaCancel(Resource):
    """
    Cancel and return home
    """
    def get(self, name):
        robot = GetRobot(name)
        robot.EndCleaning()
        robot.ReturnHome()
        return {}

@ns.route("/<string:name>/status")
class RoombaStatus(Resource):
    """
    Get the current status of a roomba
    """
    def get(self, name):
        return GetRobot(name).GetStatus()

@ns.route("/<string:name>/schedule")
class RoombaSchedule(Resource):
    """
    Get the cleaning schedule of a roomba
    """
    def get(self, name):
        return GetRobot(name).GetSchedule()
