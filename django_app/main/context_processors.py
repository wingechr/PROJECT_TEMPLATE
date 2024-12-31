from django.conf import settings
from main import __version__


def add_context(request):
    return {
        "SITE_TITLE": settings.SITE_TITLE,
        "VERSION": __version__,
        "ALLOW_REGISTER": settings.ALLOW_REGISTER,
        "ALLOW_PASSWORD_RESET": settings.ALLOW_PASSWORD_RESET,
    }
