#!/bin/bash
# requires build.sh to run first

. venv/bin/activate
python django_app/manage.py test
