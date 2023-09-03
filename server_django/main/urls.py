from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.renderers import JSONOpenAPIRenderer
from rest_framework.schemas import get_schema_view

from . import api, views

urlpatterns = []

# LOGIN (use admin)

urlpatterns += [
    path(
        "accounts/login/",
        LoginView.as_view(
            template_name="admin/login.html",
            extra_context={
                "title": admin.site.index_title,
                "site_title": admin.site.site_title,
                "site_header": admin.site.site_header,
            },
        ),
        name="login",
    ),
    path("accounts/logout/", LogoutView.as_view(), name="logout"),
]

# ADMIN

if settings.ALLOW_ADMIN:
    admin.site.site_header = settings.SITE_TITLE
    admin.site.site_title = None
    admin.site.index_title = settings.SITE_TITLE
    admin.site.site_url = None  # remove "View Site" link

    urlpatterns.append(path("admin/", admin.site.urls))

# STATIC / MEDIA

if settings.DEBUG:  # also serve static files from media
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()


class MyJSONOpenAPIRenderer(JSONOpenAPIRenderer):
    pass


# NOTE: returns forbidden if no api url registered
urlpatterns += [
    path("api/v1/", include(api.api_router.urls)),
    path(
        "openapi.json",
        get_schema_view(renderer_classes=[MyJSONOpenAPIRenderer]),
        name="openapi-schema",
    ),
    path(
        "apidoc/",
        TemplateView.as_view(
            template_name="main/apidoc.html",
            extra_context={"schema_url": "openapi-schema"},
        ),
        name="apidoc",
    ),
]

# MAIN APP

urlpatterns += [
    path("", views.index, name="index"),
]
