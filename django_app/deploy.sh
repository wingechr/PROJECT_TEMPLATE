#!/bin/bash
# requires build.sh to run first, requires variable DEPLOY_PATH

if [[ -z "${DEPLOY_PATH}" ]]; then
    echo "DEPLOY_PATH is not defined" >&2
    exit 1
fi
mkdir -p "$DEPLOY_PATH"

# copy app and build data
rsync -au --exclude "**/__pycache__" --delete app "$DEPLOY_PATH"
rsync -au --delete venv "$DEPLOY_PATH"
rsync -au --delete _static "$DEPLOY_PATH"

pushd "$DEPLOY_PATH"
. venv/bin/activate
# copy default settings if not exist
mkdir -p _local_data
test -e _local_data/local_settings.py || cp app/local_settings.example.py _local_data/local_settings.py
# update deploy system
# NOTE: ignore warnings that node_modules in the STATICFILES_DIRS setting does not exist
# we have copied already all static files
python app/manage.py migrate
python app/manage.py create_default_users # does nothing if already exist

# restart
touch app/wsgi.py
popd
