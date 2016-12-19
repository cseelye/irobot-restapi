FROM cseelye/rpi-nginx-uwsgi-flask:latest
COPY mykey.crt /etc/ssl/nginx.crt
COPY mykey.key /etc/ssl/nginx.key
COPY irobot_restapi /app
RUN pip install -U -r /app/requirements.txt

