#!/bin/bash
# requires build.sh to run first

. venv/bin/activate
python app/manage.py test
