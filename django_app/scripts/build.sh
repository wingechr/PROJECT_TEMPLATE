#!/bin/bash
# Build: create venv and _static

test -e venv || python -m venv venv
. venv/bin/activate
pushd django_app
pip install -r requirements.txt
# node/npm
npm install --no-save --omit=dev --prefix ..
# copy default settings
mkdir -p ../_local_data
cp local_settings.example.py ../_local_data/local_settings.py
python manage.py collectstatic --noinput
python manage.py compress
# TODO:translations python manage.py compilemessages
popd
