# README

webapp using django

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser


npx parcel build --target browser --dist-dir main/static

python manage.py generateschema  --format=openapi-json --file main/static/api/schema.json --title title --api_version 1.0.0



# python manage.py dumpdata -o data.json
# python manage.py loaddata

# python manage.py compress
python manage.py collectstatic --no-input
python manage.py runserver

python manage.py test

```

```config
WSGIApplicationGroup %{GLOBAL}
WSGIDaemonProcess $PROC_NAME user=$USER processes=1 threads=15 python-path=$PATH:$BASE_DIR/.env/lib/$PYTHON/site-packages home=$BASE_DIR
WSGIScriptAlias $BASE_URL $BASE_DIR/main/wsgi.py process-group=$PROC_NAME
Alias $BASE_URL/static/ $BASE_DIR/_local/static/
Alias $BASE_URL/media/ $BASE_DIR/_local/media/
```
