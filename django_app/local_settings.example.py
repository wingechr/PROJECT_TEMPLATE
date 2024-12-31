import os

__all__ = [
    "ADMIN_PASSWORD",
    "ADMIN_TOKEN",
    "ALLOWED_HOSTS",
    "BASE_URL",
    "DEBUG",
    "DEFAULT_DATABASE",
    "LOCAL_DATA_DIR",
    "LOGFILE",
    "SECRET_KEY",
    "ADMIN_NAME",
    "TESTUSER_NAME",
    "TESTUSER_MAIL",
]

DEBUG = False

LOCAL_DATA_DIR = os.path.dirname(os.path.abspath(__file__))
os.makedirs(LOCAL_DATA_DIR + "/database", exist_ok=True)

BASE_URL = "/"  # start and ends with /


SECRET_KEY = "TODO:SECRET_KEY"
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "TODO:example.com"]

ADMIN_PASSWORD = "TODO:ADMIN_PASSWORD"
ADMIN_TOKEN = "TODO:ADMIN_TOKEN"
ADMIN_EMAIL = "TODO:ADMIN_EMAIL@example.com"
DEFAULT_FROM_EMAIL = ADMIN_EMAIL
TESTUSER_PASSWORD = "TODO:TESTUSER_PASSWORD"
ADMIN_NAME = "admin"
TESTUSER_NAME = "test"
TESTUSER_MAIL = "test@example.com"


_DEFAULT_DATABASE_SQLITE = {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": LOCAL_DATA_DIR + "/database/db.sqlite3",
}
_TEST_DATABASE_SQLITE = {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": LOCAL_DATA_DIR + "/database/db.test.sqlite3",
}

_DEFAULT_DATABASE_POSTGRES = {
    "ENGINE": "django.db.backends.postgresql",
    "NAME": "TODO:DATABASE",
    "USER": "TODO:USER",
    "PASSWORD": "TODO:PASSWORD",
    "HOST": "localhost",
    "PORT": "5432",
}
_TEST_DATABASE_POSTGRES = {
    "ENGINE": "django.db.backends.postgresql",
    # "NAME": "test",
    "USER": "test",
    "PASSWORD": "test",
    "HOST": "localhost",
    "PORT": "5433",
}


DEFAULT_DATABASE = _DEFAULT_DATABASE_SQLITE
TEST_DATABASE = _TEST_DATABASE_SQLITE

LOGFILE = LOCAL_DATA_DIR + "/logs/django.log"
