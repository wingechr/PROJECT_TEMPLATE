# coding: utf-8
# coding: utf-8
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path  # noqa
from rest_framework import routers
from rest_framework.documentation import include_docs_urls

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


# REST API: extend routers from apps
api_router = routers.DefaultRouter()

for prefix, view in api.routes:
    api_router.register(prefix, view)


urlpatterns += [
    path("api/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/", include_docs_urls(title="My API service"), name="api-docs"),
    path("api/", include(api_router.urls)),
]

# MAIN APP

urlpatterns += [
    path("", views.index, name="index"),
    path("_index.html", views._index, name="_index"),
]
