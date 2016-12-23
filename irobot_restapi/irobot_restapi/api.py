#!/usr/bin/env python2.7

from flask_restplus import Api
import os

doc = False
if os.getenv("ENABLE_SWAGGERUI", "false").lower() == "true":
    doc = "/"

flask_api = Api(version="1.0",
                title="iRobot API",
                description="An API for basic control of iRobot cleaning robots",

                # Set to False in production to disable swagger UI
                doc=doc
                )
