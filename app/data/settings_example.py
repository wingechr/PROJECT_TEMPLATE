import os

__all__ = [
    "ADMIN_PASSWORD",
    "ADMIN_TOKEN",
    "ALLOW_ADMIN",
    "ALLOW_BROWSER_API",
    "ALLOWED_HOSTS",
    "BASE_URL",
    "DEBUG",
    "DEFAULT_DATABASE",
    "LANGUAGE_CODE",
    "LOCAL_DIR",
    "LOGFILE",
    "SECRET_KEY",
    "TEST_DATABASE",
    "TIME_ZONE",
]

DEBUG = True

LOCAL_DIR = os.path.dirname(os.path.abspath(__file__))

BASE_URL = "/"  # start and ends with /

LANGUAGE_CODE = "en-US"
TIME_ZONE = "Europe/Berlin"

SECRET_KEY = "**********************************"
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "my.domain.com"]
ALLOW_BROWSER_API = True
ALLOW_ADMIN = True

ADMIN_PASSWORD = "***"
ADMIN_TOKEN = "***"

SQLITE_DATABASE = {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": LOCAL_DIR + "/database/db.sqlite3",
}

POSTGRES_DATABASE = {
    "ENGINE": "django.db.backends.postgresql",
    "NAME": "<DATABASE>",
    "USER": "<USER>",
    "PASSWORD": "<PASSWORD>",
    "HOST": "localhost",
    "PORT": "5432",
}

TEST_DATABASE = {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": LOCAL_DIR + "/database/test_db.sqlite3",
}

LOGFILE = LOCAL_DIR + "/logs/log.txt"

DEFAULT_DATABASE = SQLITE_DATABASE
