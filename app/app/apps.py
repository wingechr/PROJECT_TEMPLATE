from django.apps import AppConfig
from django.conf import settings


class AppConfig(AppConfig):
    name = "app"
    verbose_name = settings.SITE_TITLE
