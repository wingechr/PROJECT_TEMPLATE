#!/bin/bash
# Build: create venv and _static

test -e venv || python -m venv venv
. venv/bin/activate
pip install -r django_app/requirements.txt
# node/npm
npm install --no-save --omit=dev file:django_app
# copy default settings
mkdir -p _local_data
cp django_app/local_settings.example.py _local_data/local_settings.py
python django_app/manage.py collectstatic --noinput
python django_app/manage.py compress
# TODO:translations python django_app/manage.py compilemessages
