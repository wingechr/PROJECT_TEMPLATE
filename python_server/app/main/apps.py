"""Register app."""

from django.apps import AppConfig
from django.conf import settings


class AppConfig(AppConfig):
    """app meta data"""

    name = "main"
    verbose_name = settings.SITE_TITLE
