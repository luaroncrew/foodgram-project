#!/bin/sh

python manage.py migrate --no-input
python manage.py collectstatic --no-input
python manage.py loaddata fixtures.json

gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
