# README

## Development

### Inital setup

- https://docs.djangoproject.com/en/5.1/intro/tutorial01/

```bash
python -m django --version # 5.1
django-admin startproject app
cd app
python manage.py startapp main

# create main app and merge into project
mv app/settings.py app/urls.py app/wsgi.py main
rm -r app
# manually rename "app" => "main"

python manage.py check # no issues
```
