"""Main wsgi entrypoint."""

from django.core.wsgi import get_wsgi_application
import manage  # keep in here so that paths are set corectly

__all__ = ["application", "manage"]

application = get_wsgi_application()
