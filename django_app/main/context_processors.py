from django.conf import settings
from main import __version__


def add_context(request):
    return {"SITE_TITLE": settings.SITE_TITLE, "VERSION": __version__}
