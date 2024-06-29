import logging
import sys

from _local.settings import (
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
    "drf_spectacular",  # schema generation
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


STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    # other finders..
    "compressor.finders.CompressorFinder",
)


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
node_path = "../node_modules"
STATICFILES_DIRS = [
    ("vendor", f"{node_path}/@popperjs/core/dist/umd"),
    ("vendor", f"{node_path}/jquery/dist"),
    ("vendor", f"{node_path}/bootstrap/dist"),
    ("vendor", f"{node_path}/bootstrap-icons/font"),
    ("vendor", f"{node_path}/bootstrap-select/dist"),
    ("vendor", f"{node_path}/swagger-ui/dist"),
    ("vendor", f"{node_path}/swagger-client/dist"),
    ("vendor", f"{node_path}/@wingechr/javascript_frontend/dist/static"),
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


# all must end in slash
STATIC_URL = BASE_URL + "static/"  # noqa: F405: local setting
STATIC_ROOT = LOCAL_DIR + "/static/"

MEDIA_URL = BASE_URL + "media/"  # noqa: F405: local setting
MEDIA_ROOT = LOCAL_DIR + "/media/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_PASSWORD_VALIDATORS = []

AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend"]  # default

LOGIN_URL = BASE_URL + "admin/login"
LOGOUT_URL = BASE_URL + "admin/logout"

# https://django-compressor.readthedocs.io/en/stable/settings.html#django.conf.settings.COMPRESS_OFFLINE
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True

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
