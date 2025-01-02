#!/bin/bash
# Build: create venv and _static

test -e venv || python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
# node/npm
npm install --no-save --omit=dev
# copy default settings
mkdir -p _local_data
cp app/local_settings.example.py _local_data/local_settings.py
python app/manage.py collectstatic --noinput
python app/manage.py compress
# TODO:translations python app/manage.py compilemessages
