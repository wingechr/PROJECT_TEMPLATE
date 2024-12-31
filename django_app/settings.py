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
    DEBUG,
    DEFAULT_DATABASE,
    DEFAULT_FROM_EMAIL,
    LOCAL_DATA_DIR,
    LOGFILE,
    SECRET_KEY,
    TEST_DATABASE,
    TESTUSER_MAIL,
    TESTUSER_NAME,
    TESTUSER_PASSWORD,
)

__all__ = [
    "ADMIN_PASSWORD",
    "ADMIN_TOKEN",
    "ADMIN_EMAIL",
    "ALLOWED_HOSTS",
    "SECRET_KEY",
    "DEFAULT_FROM_EMAIL",
    "TESTUSER_PASSWORD",
    "ADMIN_NAME",
    "TESTUSER_NAME",
    "TESTUSER_MAIL",
]

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
    "rest_framework",
    "rest_framework.authtoken",
    "compressor",  # hashed static files
    "htmlmin",  # TODO: error in debug?
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
    # from django-htmlmin
    "htmlmin.middleware.HtmlMinifyMiddleware",
    "htmlmin.middleware.MarkRequestMiddleware",
]


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
node_modules = ROOT_DIR + "/node_modules"  # relative to workdir
STATICFILES_DIRS = [
    ("vendor/popperjs", f"{node_modules}/@popperjs/core/dist/umd"),
    ("vendor/bootstrap", f"{node_modules}/bootstrap/dist"),
    ("vendor/bootstrap-icons", f"{node_modules}/bootstrap-icons/font"),
    ("vendor/fontawesome", f"{node_modules}/@fortawesome/fontawesome-free"),
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

DATABASES = {"default": TEST_DATABASE if "test" in sys.argv else DEFAULT_DATABASE}

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
