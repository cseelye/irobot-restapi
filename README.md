# irobot-restapi
REST API for iRobot cleaning robots written in python and Flask.

I built this API as an endpoint for an Alexa skill so that I can control my roomba via voice commands. This is basically a Docker container with a REST wrapper around my [pyirobot](https://pypi.python.org/pypi/pyirobot) module with just the action commands exposed. If you are going to expose this API to the internet, make sure you put it behind an SSL proxy!

Swagger UI is available but disabled by default.  You can turn it on with an environment variable so you can easily explore and test the API. Make sure to keep it off if you connect this API to the internet!

To use this API you will need to have your robot's IP address and password. The IP is best set using a DHCP reservation on your router; see my [pyirobot](https://pypi.python.org/pypi/pyirobot) module for how to obtain the password.


### Usage

The easiest way to set up this API is to use the Docker container.
* Download [robotconfig_sample.json](irobot_restapi/irobot_restapi/robotconfig_sample.json) and [userconfig_sample.json](irobot_restapi/irobot_restapi/userconfig_sample.json) and rename them to robotconfig.json and userconfig.json.
* Edit the two files and enter in your robot's information, and a username/password you would like to use for the API.

At this point, you can either create your own image with your files built in, or run this image and mount your files into the correct places.

* Create a Dockerfile to build your config files into the image:

    ```
    FROM cseelye/irobot-restapi
    COPY robotconfig.json userconfig.json /app/irobot_restapi/
    ```

* Or if you are running on a Raspberry Pi, use the rpi base container:

    ```
    FROM cseelye/rpi-irobot-restapi
    COPY robotconfig.json userconfig.json /app/irobot_restapi/
    ```

Build the image:  
```docker build -t robotapi .```

Run the image on a custom port:  
```docker run -p 12345:80 --env ENABLE_SWAGGERUI=true robotapi```

Open http://localhost:12345 and browse the API
