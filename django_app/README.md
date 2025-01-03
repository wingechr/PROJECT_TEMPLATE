# README

## Development

make sure that `_local_data` and `django_app` are in your `PYTHONPATH`, so that your
IDE works properly

## Deployment - Setup

### Database

```sql sudo -u postgres psql
CREATE USER $USER WITH PASSWORD '$PASSWORD';
CREATE DATABASE $DATABASE OWNER $USER;
```

- make sure user is also allowed in ` /etc/postgresql/$PGVERSION/main/pg_hba.conf`
- test: `psql postgres://$USER:$PASSWORD@localhost:5432/$DATABASE`

### Webserver

```conf /etc/apache2/sites-available/$DOMAIN.conf
<IfModule ssl_module>
<VirtualHost *:443>

ServerName $DOMAIN

SSLCertificateFile    /etc/letsencrypt/live/$DOMAIN/fullchain.pem
SSLCertificateKeyFile /etc/letsencrypt/live/$DOMAIN/privkey.pem
SSLEngine on

LogLevel warn
ErrorLog ${APACHE_LOG_DIR}/$DOMAIN/error.log
CustomLog ${APACHE_LOG_DIR}/$DOMAIN/access.log combined

WSGIPassAuthorization On
WSGIDaemonProcess $NAME user=www-data processes=1 threads=5 display-name=$NAME python-path=$DEPLOY_PATH/venv/lib/python3.11/site-packages home=$DEPLOY_PATH/app
WSGIScriptAlias / $DEPLOY_PATH/app/wsgi.py process-group=$NAME
Alias /static/ $DEPLOY_PATH/_static/
# NOTE: serve media from django we can have access control
<Location />
    Require all granted
    Allow from all
</Location>
<Directory $DEPLOY_PATH/_static>
    Require all granted
    Allow from all
</Directory>

</VirtualHost>
</IfModule>

# Redirect
<VirtualHost *:80>
    ServerName $DOMAIN
    Redirect permanent / https://$DOMAIN/
</VirtualHost>
```

- install cert: `sudo certbot certonly --apache -d $DOMAIN`
- enabble site: `sudo a2ensite $DOMAIN`

### Folder structure

```bash su www-data

mkdir -p /var/www/html/$DOMAIN/html/static
mkdir -p /var/www/html/$DOMAIN/local_data/media
mkdir -p /var/www/html/$DOMAIN/local_data/database
mkdir -p /var/www/html/$DOMAIN/dlocal_dataata/backups
mkdir -p /var/www/html/$DOMAIN/local_data/static
mkdir -p /var/log/apache2/$DOMAIN
ln -s /var/log/apache2/$DOMAIN /var/www/html/$DOMAIN/local_data/logs
ln -s /var/www/html/$DOMAIN/local_data/media /var/www/html/$DOMAIN/html/media
ln -s /var/www/html/$DOMAIN/local_data/static /var/www/html/$DOMAIN/html/static

pushd /var/www/html/$DOMAIN # goto workdir

python -m venv venv
```

- also copy modified `app/settings_example.py` to `local_data/settings.py`

## Deployment - Update

```bash
pushd /var/www/html/$DOMAIN # goto workdir
. venv/bin/activate
pip install -r app/requirements.txt
npm install --no-save file:django_app

export PYTHONPATH=$(pwd)
python app/manage.py check
python app/manage.py migrate
python app/manage.py spectacular --format=openapi-json --file app/main/static/api/schema.json
python app/manage.py collectstatic --no-input
python app/manage.py compress
python app/manage.py create_admin

touch app/wsgi.py # restart
```

## Development

```bash
python app/manage.py makemigrations
python app/manage.py test
python app/manage.py runserver
python app/manage.py dumpdata -o local_data/backups/data.json
python app/manage.py loaddata local_data/backups/data.json
```
