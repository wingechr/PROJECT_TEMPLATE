import logging
import os
import sys

from django.contrib.messages import constants as messages

# local_settings.py in LOCAL_DATA_DIR
from local_settings import (
    ADMIN_EMAIL,
    ADMIN_NAME,
    ADMIN_PASSWORD,
    ADMIN_TOKEN,
    ALLOWED_HOSTS,
    BASE_URL,
    CORS_ALLOWED_ORIGINS,
    DEFAULT_FROM_EMAIL,
    LOCAL_DATA_DIR,
    LOGFILE,
    PRODUCTION,
    PRODUCTION_DATABASES,
    SECRET_KEY,
    TEST_DATABASES,
    TESTUSER_MAIL,
    TESTUSER_NAME,
    TESTUSER_PASSWORD,
)

# imported but used elsewhere
__all__ = [
    ADMIN_EMAIL,
    ADMIN_NAME,
    ADMIN_PASSWORD,
    ADMIN_TOKEN,
    ALLOWED_HOSTS,
    DEFAULT_FROM_EMAIL,
    SECRET_KEY,
    TESTUSER_MAIL,
    TESTUSER_NAME,
    TESTUSER_PASSWORD,
    CORS_ALLOWED_ORIGINS,
]

DEBUG = not PRODUCTION
IS_TEST = ("test" in sys.argv) and (not PRODUCTION)

# ROOT_DIR: contains node_modules, django_app, _static
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SITE_TITLE = "TODO:SITE_TITLE"

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
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "drf_spectacular",  # open api schema
    "drf_spectacular_sidecar",  # required for Django collectstatic discovery
    "django_filters",
    "compressor",  # hashed static files
    "htmlmin",
    # our apps
    "main.apps.AppConfig",
    "data.apps.AppConfig",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # must be first
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # from django-htmlmin
    "htmlmin.middleware.HtmlMinifyMiddleware",
    "htmlmin.middleware.MarkRequestMiddleware",
]

# CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]

REST_FRAMEWORK = {
    # https://www.django-rest-framework.org/api-guide/permissions/
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
        # "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        # 'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_THROTTLE_RATES": {"anon": "24/day", "user": "86400/day"},
    "DEFAULT_PAGINATION_CLASS": None,
    "PAGE_SIZE": None,
}

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    # other finders..
    "compressor.finders.CompressorFinder",
)

SPECTACULAR_SETTINGS = {
    "TITLE": SITE_TITLE,
    "DESCRIPTION": "TODO:DESCRIPTION",
    "VERSION": "0.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    # OTHER SETTINGS
    "SWAGGER_UI_DIST": "SIDECAR",  # shorthand to use the sidecar instead
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
}

STATICFILES_IGNORE_PATTERNS = [
    # we dont need this one and it has invalid references
    # to missing vendor/short-unique-id.js.map
    # r".*swagger-client.browser.js$",
]

# add node_modules folders: prefix => path
# NOTE: we dont need this in production, because we use collected static files
if not PRODUCTION:
    node_modules = ROOT_DIR + "/node_modules"  # relative to workdir
    STATICFILES_DIRS = [
        ("vendor/popperjs", f"{node_modules}/@popperjs/core/dist/umd"),
        ("vendor/bootstrap", f"{node_modules}/bootstrap/dist"),
        ("vendor/bootstrap-icons", f"{node_modules}/bootstrap-icons/font"),
        ("vendor/fontawesome", f"{node_modules}/@fortawesome/fontawesome-free"),
    ]
else:
    STATICFILES_DIRS = []

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
                "main.context_processors.add_context",
            ]
        },
    }
]

# messages as bootstrap classes
MESSAGE_TAGS = {
    messages.DEBUG: "alert-info",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}

ROOT_URLCONF = "urls"
WSGI_APPLICATION = "wsgi.application"

# NOTE: using "TEST" keyword in database does not allow for choosing a different
# port, so we do it like this
DATABASES = TEST_DATABASES if IS_TEST else PRODUCTION_DATABASES


# data for app "data"  is in separate database
DATABASE_ROUTERS = ["data.routers.DataAppDatabaseRouter"]

# LOCALE_PATHS = ["main/locale"]

USE_I18N = True  # internationalization
USE_L10N = True  # localization
USE_TZ = True

# Languages available for the app
LANGUAGES = [
    ("en", "English"),
    # ("de", "German"),
]


# all must end in slash
# LOCAL_DATA_DIR: contains local_settings.py and media
STATIC_URL = BASE_URL + "static/"
STATIC_ROOT = ROOT_DIR + "/_static/"
MEDIA_URL = BASE_URL + "media/"
MEDIA_ROOT = LOCAL_DATA_DIR + "/media/"

os.makedirs(MEDIA_ROOT, exist_ok=True)
os.makedirs(STATIC_ROOT, exist_ok=True)

APPEND_SLASH = False

# these are the default values
# https://docs.djangoproject.com/en/5.1/ref/settings/

# NOTE: using admin login restricts login to users with at least staff status
# LOGIN_URL = BASE_URL + "admin/login/"
LOGIN_URL = BASE_URL + "accounts/login/"
LOGIN_REDIRECT_URL = BASE_URL + "accounts/profile/"
# custom
LOGOUT_URL = BASE_URL + "accounts/logout/"
LOGOUT_REDIRECT_URL = BASE_URL  # index


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# use local postfix
EMAIL_HOST = "localhost"
EMAIL_PORT = 25
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# custom user model (auth.User is the default)
AUTH_USER_MODEL = "main.User"

AUTH_PASSWORD_VALIDATORS = []
AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend"]  # default

# https://pypi.org/project/django-htmlmin/
HTML_MINIFY = not DEBUG  # we also want to test local minification + validation

# https://django-compressor.readthedocs.io/en/stable/settings.html
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = not DEBUG  # offline in production

COMPRESS_FILTERS = {
    # do not minify js, we do it with parcel
    # and it can create problems with react
    "js": [],
    # we minify with parcel, but we need to pass it
    # through CssAbsoluteFilter to resolve linked fonts
    "css": [
        "compressor.filters.css_default.CssAbsoluteFilter",
        # "compressor.filters.cssmin.rCSSMinFilter",
    ],
}


ALLOW_REGISTER = True
ALLOW_PASSWORD_RESET = True

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
