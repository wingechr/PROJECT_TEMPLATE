import logging
import os
import sys
from os.path import abspath, dirname

# root_dir contains _local
root_dir = dirname(dirname(dirname(abspath(__file__))))
sys.path.insert(0, root_dir)

from _local.settings import (  # noqa E402
    ADMIN_PASSWORD,
    ADMIN_TOKEN,
    ALLOW_ADMIN,
    ALLOW_BROWSER_API,
    ALLOWED_HOSTS,
    BASE_URL,
    DEBUG,
    DEFAULT_DATABASE,
    LANGUAGE_CODE,
    LOCAL_DIR,
    LOGFILE,
    SECRET_KEY,
    TEST_DATABASE,
    TIME_ZONE,
)

# unused here but used in app
__all__ = [
    "ADMIN_PASSWORD",
    "ADMIN_TOKEN",
    "ALLOW_ADMIN",
    "ALLOW_BROWSER_API",
    "ALLOWED_HOSTS",
    "LANGUAGE_CODE",
    "SECRET_KEY",
    "TIME_ZONE",
]


SITE_TITLE = "TITLE"

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
    "django_filters",
    "drf_spectacular",  # schema generation
    "drf_spectacular_sidecar",
    "compressor",  # hashed static files
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
    # "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.openapi.AutoSchema",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        # 'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
}

SPECTACULAR_SETTINGS = {
    "TITLE": "TODO: TITLE",
    "DESCRIPTION": "TODO: DESCRIPTION",
    "VERSION": "0.0.1",
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_DIST": "SIDECAR",  # shorthand to use the sidecar instead
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
    "COMPONENT_SPLIT_PATCH": True,
}

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    # other finders..
    "compressor.finders.CompressorFinder",
)


STATICFILES_IGNORE_PATTERNS = [
    # we dont need this one and it has invalid references
    # to missing vendor/short-unique-id.js.map
    # r".*swagger-client.browser.js$",
]
STATICFILES_STORAGE = "main.static.ManifestStaticFilesStorageWithIgnore"


# add node_modules folders: prefix => path
node_path = "../../node_modules"
STATICFILES_DIRS = [
    (
        "vendor",
        f"{node_path}/@wingechr/javascript_frontend/dist/static",
    ),
    ("vendor", f"{node_path}/@popperjs/core/dist/umd"),
    ("vendor", f"{node_path}/jquery/dist"),
    ("vendor", f"{node_path}/bootstrap/dist"),
    ("vendor", f"{node_path}/bootstrap-icons/font"),
    ("vendor", f"{node_path}/bootstrap-select/dist"),
    ("vendor", f"{node_path}/swagger-ui/dist"),
    ("vendor", f"{node_path}/swagger-client/dist"),
]

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


ROOT_URLCONF = "main.urls"
WSGI_APPLICATION = "wsgi.application"

if "test" in sys.argv:
    DATABASES = {"default": TEST_DATABASE}  # noqa: F405: local setting
else:
    DATABASES = {"default": DEFAULT_DATABASE}  # noqa: F405: local setting

USE_I18N = True
USE_L10N = True
USE_TZ = True


# all must end in slash
STATIC_URL = BASE_URL + "static/"  # noqa: F405: local setting
STATIC_ROOT = LOCAL_DIR + "/static/"

MEDIA_URL = BASE_URL + "media/"  # noqa: F405: local setting
MEDIA_ROOT = LOCAL_DIR + "/media/"

os.makedirs(MEDIA_ROOT, exist_ok=True)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_PASSWORD_VALIDATORS = []

AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend"]  # default

LOGIN_URL = BASE_URL + "admin/login"
LOGOUT_URL = BASE_URL + "admin/logout"

# https://django-compressor.readthedocs.io/en/stable/settings.html
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
# default is CACHE
# COMPRESS_OUTPUT_DIR = "CACHE"

# Logging
LOGLEVEL = logging.INFO if DEBUG else logging.WARNING  # noqa: F405: local setting
logger = logging.getLogger()
logFormatter = logging.Formatter(
    "[%(asctime)s %(levelname)7s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
fileHandler = logging.FileHandler(LOGFILE, encoding="utf-8")
fileHandler.setFormatter(logFormatter)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.setLevel(LOGLEVEL)
logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)
