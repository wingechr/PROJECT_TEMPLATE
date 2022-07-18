# coding: utf-8

import logging
import os
import sys
from urllib.parse import urljoin

from _local.settings import *  # noqa: F403

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd party
    "rest_framework",
    "rest_framework.authtoken",
    "guardian",  # object based permissions
    # apps
    "main.apps.AppConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# https://www.django-rest-framework.org/api-guide/permissions/
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
}


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

# add node_modules folders: prefix => path
STATICFILES_DIRS = [
    ("vendor", "node_modules/jquery/dist"),
    ("vendor", "node_modules/bootstrap/dist"),
    ("vendor", "node_modules/bootstrap-icons/font"),
    ("vendor", "node_modules/bootstrap-select/dist"),
]


ROOT_URLCONF = "main.urls"
WSGI_APPLICATION = "main.wsgi.application"

if "test" in sys.argv:
    DATABASES = {"default": TEST_DATABASE}  # noqa: F405: local setting
else:
    DATABASES = {"default": DEFAULT_DATABASE}  # noqa: F405: local setting

USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = urljoin(BASE_URL, "static/")  # noqa: F405: local setting
STATIC_ROOT = os.path.join(BASE_DIR, "_static/")

MEDIA_URL = urljoin(BASE_URL, "media/")  # noqa: F405: local setting
MEDIA_ROOT = os.path.join(BASE_DIR, "_local/media/")


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_PASSWORD_VALIDATORS = []

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",  # default
    "guardian.backends.ObjectPermissionBackend",
)

LOGLEVEL = logging.INFO if DEBUG else logging.WARNING  # noqa: F405: local setting
logger = logging.getLogger()
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s %(funcName)s] %(message)s")
fileHandler = logging.FileHandler(os.path.join(BASE_DIR, "_local", "log.txt"))
fileHandler.setFormatter(logFormatter)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.setLevel(LOGLEVEL)
logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)
