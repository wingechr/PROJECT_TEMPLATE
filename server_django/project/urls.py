# coding: utf-8
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, logout
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

admin.site.site_header = settings.SITE_TITLE
admin.site.site_title = None
admin.site.index_title = settings.SITE_TITLE
admin.site.site_url = None  # remove "View Site" link

urlpatterns = [
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
    path("accounts/logout/", logout, name="logout"),
    path("api/get_token/", obtain_auth_token, name="get_token"),
    path("", include("main.urls")),
]

if settings.ALLOW_ADMIN:
    urlpatterns.append(path("admin/", admin.site.urls))

if settings.ALLOW_BROWSER_API:
    urlpatterns.append(
        path("api/auth/", include("rest_framework.urls", namespace="rest_framework"))
    )

if settings.DEBUG:  # also serve static files from media
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
