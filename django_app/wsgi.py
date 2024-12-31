# coding: utf-8
import manage  # keep in here so that paths are set corectly
from django.core.wsgi import get_wsgi_application

__all__ = ["application", "manage"]

application = get_wsgi_application()
