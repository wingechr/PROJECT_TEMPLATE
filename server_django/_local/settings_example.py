# coding: utf-8
import os

LOCAL_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BASE_URL = "/"  # start and ends with /
SITE_TITLE = "TITLE"
LANGUAGE_CODE = "en-US"
TIME_ZONE = "Europe/Berlin"
DEBUG = True
SECRET_KEY = "**********************************"
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "my.domain.com"]
ALLOW_BROWSER_API = True
ALLOW_ADMIN = True

DBNAME = SITE_TITLE.lower().replace(" ", "")

SQLITE_DATABASE = {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": LOCAL_BASE_DIR + "/db.sqlite3",
}

TEST_DATABASE = {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": LOCAL_BASE_DIR + "/test_db.sqlite3",
}

DEFAULT_DATABASE = SQLITE_DATABASE
