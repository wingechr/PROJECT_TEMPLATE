```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

python manage.py collectstatic --no-input
python manage.py test
python manage.py runserver
```

```config
WSGIApplicationGroup %{GLOBAL}
WSGIDaemonProcess $PROC_NAME user=www-data processes=1 threads=15 python-path=$PATH:$BASE_DIR/.env/lib/$PYTHON/site-packages home=$BASE_DIR
WSGIScriptAlias $BASE_URL $BASE_DIR/main/wsgi.py process-group=$PROC_NAME
Alias $BASE_URL/static/ $BASE_DIR/_static/
Alias $BASE_URL/media/ $BASE_DIR/_local/media/
```
