"""Add variables to every context passed to templates."""

from django.conf import settings
from main import __version__


def add_context(request):
    """Add variables to every context passed to templates."""
    return {
        "SITE_TITLE": settings.SITE_TITLE,
        "VERSION": __version__,
        "ALLOW_REGISTER": settings.ALLOW_REGISTER,
        "ALLOW_PASSWORD_RESET": settings.ALLOW_PASSWORD_RESET,
    }
