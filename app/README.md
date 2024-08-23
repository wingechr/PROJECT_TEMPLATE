# README

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

ErrorLog /var/log/apache2/$DOMAIN/error.log
CustomLog /var/log/apache2/$DOMAIN/access.log combined

SSLCertificateFile    /etc/letsencrypt/live/$DOMAIN/fullchain.pem
SSLCertificateKeyFile /etc/letsencrypt/live/$DOMAIN/privkey.pem
SSLEngine on

DocumentRoot /var/www/html/$DOMAIN/html

<Directory /var/www/html/$DOMAIN/html>
    Options FollowSymLinks
    AllowOverride All
    Require all granted
    Order Allow,Deny
    Allow from all
</Directory>

<LocationMatch ".*/\.">
    Require all denied
    Deny from all
</LocationMatch>

WSGIApplicationGroup %{GLOBAL}

WSGIDaemonProcess $NAME user=www-data processes=1 threads=15 python-path=/var/www/html/$DOMAIN/venv/lib/$PYTHON/site-packages:/var/www/html/$DOMAIN/app home=/var/www/html/$DOMAIN/app
WSGIScriptAlias $PREFIX/ /var/www/html/$DOMAIN/app/wsgi.py process-group=$NAME
# these will be symlinks:
Alias $PREFIX/static/ /var/www/html/$DOMAIN/html/static/
Alias $PREFIX/media/ /var/www/html/$DOMAIN/html/media/
WSGIPassAuthorization On

</VirtualHost>
</IfModule>

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
mkdir -p /var/www/html/$DOMAIN/data/media
mkdir -p /var/www/html/$DOMAIN/data/database
mkdir -p /var/www/html/$DOMAIN/data/backups
mkdir -p /var/www/html/$DOMAIN/data/static
mkdir -p /var/log/apache2/$DOMAIN
ln -s /var/log/apache2/$DOMAIN /var/www/html/$DOMAIN/data/logs
ln -s /var/www/html/$DOMAIN/data/media /var/www/html/$DOMAIN/html/media
ln -s /var/www/html/$DOMAIN/data/static /var/www/html/$DOMAIN/html/static

pushd /var/www/html/$DOMAIN # goto workdir

python -m venv venv
```

- also copy modified `data/settings_example.py` to `data/settings.py`

## Deployment - Update

```bash
pushd /var/www/html/$DOMAIN # goto workdir
. venv/bin/activate
pip install -r app/requirements.txt
npm install --no-save file:app

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
python app/manage.py dumpdata -o data/backups/data.json
python app/manage.py loaddata data/backups/data.json
```
