import logging
import os
import sys

from local_data.settings import (
    ADMIN_PASSWORD,
    ADMIN_TOKEN,
    ALLOWED_HOSTS,
    BASE_URL,
    DEBUG,
    DEFAULT_DATABASE,
    LOCAL_DIR,
    LOGFILE,
    SECRET_KEY,
    TEST_DATABASE,
)

__all__ = [
    "ADMIN_PASSWORD",
    "ADMIN_TOKEN",
    "ALLOWED_HOSTS",
    "SECRET_KEY",
]


SITE_TITLE = "MY SITE TITLE"

# Default timezone / language
TIME_ZONE = "UTC"
LANGUAGE_CODE = "en"

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
    "drf_spectacular_sidecar",
    "compressor",  # hashed static files
    # our apps
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
        # "rest_framework.permissions.IsAuthenticatedOrReadOnly",
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
    "TITLE": SITE_TITLE,
    "DESCRIPTION": "",
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

# add node_modules folders: prefix => path
node_modules = "../node_modules"  # relative to workdir
STATICFILES_DIRS = [
    # ("vendor", f"{node_modules}/@popperjs/core/dist/umd"),
    ("vendor/bootstrap", f"{node_modules}/bootstrap/dist"),
    ("vendor/chart.js", f"{node_modules}/chart.js/dist"),
    ("vendor/bootstrap-icons", f"{node_modules}/bootstrap-icons/font"),
    # ("vendor/bootstrap-select", f"{node_modules}/bootstrap-select/dist"),
    ("vendor/fontawesome", f"{node_modules}/@fortawesome/fontawesome-free"),
    ("vendor/swagger-ui", f"{node_modules}/swagger-ui/dist"),
    ("vendor/swagger-client", f"{node_modules}/swagger-client/dist"),
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["main/templates"],  # override default templates
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                # will be added to template context
                # you can add your own (function(request) => {})
                "django.template.context_processors.debug",  # debug
                "django.template.context_processors.csrf",  # # csrf_token
                "django.template.context_processors.request",  # request
                "django.contrib.auth.context_processors.auth",  # user, perms
                "django.contrib.messages.context_processors.messages",  # messages, DEFAULT_MESSAGE_LEVELS # noqa
                # "django.template.context_processors.static",  # STATIC_URL
                "django.template.context_processors.media",  # MEDIA_URL
                "django.template.context_processors.i18n",  # LANGUAGES,LANGUAGE_BIDI, LANGUAGE_CODE # noqa
                # CUSTOM
            ]
        },
    }
]


ROOT_URLCONF = "main.urls"
WSGI_APPLICATION = "wsgi.application"

DATABASES = {"default": TEST_DATABASE if "test" in sys.argv else DEFAULT_DATABASE}

# LOCALE_PATHS = ["main/locale"]

USE_I18N = True  # internationalization
USE_L10N = True  # localization
USE_TZ = True

# Languages available for the app
LANGUAGES = [
    ("en", "English"),
    ("de", "German"),
]


# all must end in slash
STATIC_URL = BASE_URL + "static/"
STATIC_ROOT = LOCAL_DIR + "/static/"

MEDIA_URL = BASE_URL + "media/"
MEDIA_ROOT = LOCAL_DIR + "/media/"

os.makedirs(MEDIA_ROOT, exist_ok=True)
os.makedirs(STATIC_ROOT, exist_ok=True)


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "auth.User"  # auth.User is the default


AUTH_PASSWORD_VALIDATORS = []
AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend"]  # default

# these are the default values
# https://docs.djangoproject.com/en/5.1/ref/settings/
LOGIN_URL = BASE_URL + "admin/login"
LOGIN_REDIRECT_URL = BASE_URL
# custom
LOGOUT_URL = BASE_URL + "accounts/logout"
LOGOUT_REDIRECT_URL = BASE_URL  # index

# TODO
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# https://django-compressor.readthedocs.io/en/stable/settings.html
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = False
# default is CACHE
# COMPRESS_OUTPUT_DIR = "CACHE"

# Logging
LOGLEVEL = logging.INFO if DEBUG else logging.WARNING
logger = logging.getLogger()
logFormatter = logging.Formatter(
    "[%(asctime)s %(levelname)7s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.setLevel(LOGLEVEL)
logger.addHandler(consoleHandler)
if LOGFILE:
    os.makedirs(os.path.dirname(LOGFILE), exist_ok=True)
    fileHandler = logging.FileHandler(LOGFILE, encoding="utf-8")
    fileHandler.setFormatter(logFormatter)
    logger.addHandler(fileHandler)
