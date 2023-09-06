import logging
import os
import sys

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


REST_FRAMEWORK = {
    # https://www.django-rest-framework.org/api-guide/permissions/
    "DEFAULT_PERMISSION_CLASSES": [
        # "rest_framework.permissions.IsAuthenticated",
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        # 'rest_framework.renderers.BrowsableAPIRenderer',
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
    ("vendor", "node_modules/swagger-ui/dist"),
    ("vendor", "node_modules/swagger-client/dist"),
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

LOCAL_ROOT = BASE_DIR + "/_local"

# all must end in slash
STATIC_URL = BASE_URL + "static/"  # noqa: F405: local setting
STATIC_ROOT = LOCAL_ROOT + "/static/"

MEDIA_URL = BASE_URL + "media/"  # noqa: F405: local setting
MEDIA_ROOT = LOCAL_ROOT + "/media/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_PASSWORD_VALIDATORS = []

AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend"]  # default

LOGLEVEL = logging.WARNING if DEBUG else logging.WARNING  # noqa: F405: local setting
logger = logging.getLogger()
logFormatter = logging.Formatter(
    "[%(asctime)s %(levelname)7s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
fileHandler = logging.FileHandler(
    os.path.join(BASE_DIR, "_local", "log.txt"), encoding="utf-8"
)
fileHandler.setFormatter(logFormatter)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.setLevel(LOGLEVEL)
logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)
