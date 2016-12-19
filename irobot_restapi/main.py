#!/usr/bin/env python2.7
"""
REST API to control iRobot cleaning robots
"""

from irobot_restapi import app as robot_app
app = robot_app

if __name__ == '__main__':
    app.run(debug=True)
