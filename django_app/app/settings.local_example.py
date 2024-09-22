import os

__all__ = [
    "ADMIN_PASSWORD",
    "ADMIN_TOKEN",
    "ALLOWED_HOSTS",
    "BASE_URL",
    "DEBUG",
    "DEFAULT_DATABASE",
    "LOCAL_DIR",
    "LOGFILE",
    "SECRET_KEY",
]

DEBUG = False

LOCAL_DIR = os.path.dirname(os.path.abspath(__file__))

BASE_URL = "/"  # start and ends with /


SECRET_KEY = "**********************************"
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "my.domain.com"]

ADMIN_PASSWORD = "*************************************"
ADMIN_TOKEN = "*************************************"

_DEFAULT_DATABASE_SQLITE = {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": LOCAL_DIR + "/database/db.sqlite3",
}
_TEST_DATABASE_SQLITE = {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": LOCAL_DIR + "/database/test_db.sqlite3",
}
# os.makedirs(LOCAL_DIR + "/database", exist_ok=True)


_DEFAULT_DATABASE_POSTGRES = {
    "ENGINE": "django.db.backends.postgresql",
    "NAME": "<DATABASE>",
    "USER": "<USER>",
    "PASSWORD": "<PASSWORD>",
    "HOST": "localhost",
    "PORT": "5432",
}
_TEST_DATABASE_POSTGRES = {
    "ENGINE": "django.db.backends.postgresql",
    "NAME": "django_app_test",
    "USER": "test",
    "PASSWORD": "test",
    "HOST": "localhost",
    "PORT": "5433",
}


DEFAULT_DATABASE = _DEFAULT_DATABASE_SQLITE
TEST_DATABASE = _TEST_DATABASE_SQLITE

LOGFILE = LOCAL_DIR + "/logs/log.txt"
