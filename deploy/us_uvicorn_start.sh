#!/usr/bin/env bash

NAME="2Step Url Shortener App"
DJANGODIR=/src/2step_url_shortener/url_shortener
ENVBIN=/src/us_env/bin

DJANGO_SETTINGS_MODULE=url_shortener.settings.prod

echo "Starting $NAME as whoami"

source $ENVBIN/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH
export WEB_CONCURRENCY=10
export WORKER_CLASS="uvicorn.workers.UvicornH11Worker"

exec $ENVBIN/uvicorn --host 0.0.0.0 --port 8000 url_shortener.asgi:application
