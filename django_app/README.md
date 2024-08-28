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

### Auth

- https://docs.djangoproject.com/en/5.1/topics/auth/default/

Django provides no default template for the authentication views. You should create your own templates for the views you want to use. The template context is documented in each view, see All authentication views: https://docs.djangoproject.com/en/5.1/topics/auth/default/#all-authentication-views
