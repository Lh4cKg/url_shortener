#!/usr/bin/env bash

NAME="2Step Url Shortener App"         # Name of the application
DJANGODIR=/src/2step_url_shortener/url_shortener       # Django project directory
ENVBIN=/src/us_env/bin
DJANGO_SETTINGS_MODULE=url_shortener.settings.prod   # which settings file should Django use
DJANGO_WSGI_MODULE=url_shortener.wsgi           # WSGI module name

TIMEOUT=120
echo "Starting $NAME as whoami"

# Activate the virtual environment

cd $DJANGODIR
source $ENVBIN/activate

cd $DJANGODIR
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH


## Create the run directory if it doesn't exist
#RUNDIR=$(dirname $SOCKFILE)
#test -d $RUNDIR || mkdir -p $RUNDIR

exec $ENVBIN/uwsgi --ini /src/2step_url_shortener/deploy/us_uwsgi.ini
