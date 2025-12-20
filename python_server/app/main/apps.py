"""Register app."""

from django import apps
from django.conf import settings


class AppConfig(apps.AppConfig):
    """app meta data"""

    name = "main"
    verbose_name = settings.SITE_TITLE
