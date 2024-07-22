# README

## Development

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py spectacular --format=openapi-json --file main/static/api/schema.json
python manage.py collectstatic --no-input
python manage.py test
python manage.py runserver
python manage.py migrate
python manage.py create_admin
python manage.py dumpdata -o ../_local/backups/data.json
python manage.py loaddata ../_local/backups/data.json
```

## Deployment

- copy `app` and `_local`
- create and edit `_local/settings.py`
- set up local database
- set up webserver (using `webserver` config files)
- run update
- create admin

## Deployment Update

- backup database?
- sync only `app`
- run `migration`
- run `collectstatic`
- touch `wsgi.py` for restart
