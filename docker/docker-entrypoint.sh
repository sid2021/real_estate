#!/bin/bash

case "$1" in

runserver)
  shift
  python manage.py collectstatic --noinput
  python manage.py migrate
  python manage.py runserver 0.0.0.0:8001
  ;;

gunicorn)
  shift
  python manage.py collectstatic --noinput
  python manage.py migrate
  python gunicorn config.wsgi -b 0.0.0.0:8001
  ;;

esac