```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser


npx parcel build --target main

python manage.py generateschema  --format=openapi-json --file main/static/openapi.schema.json

python manage.py collectstatic --no-input
python manage.py test
python manage.py runserver


```

```config
WSGIApplicationGroup %{GLOBAL}
WSGIDaemonProcess $PROC_NAME user=$USER processes=1 threads=15 python-path=$PATH:$BASE_DIR/.env/lib/$PYTHON/site-packages home=$BASE_DIR
WSGIScriptAlias $BASE_URL $BASE_DIR/main/wsgi.py process-group=$PROC_NAME
Alias $BASE_URL/static/ $BASE_DIR/_local/static/
Alias $BASE_URL/media/ $BASE_DIR/_local/media/
```
