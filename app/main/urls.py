from django.conf import settings
from django.contrib import admin
from django.templatetags.static import static
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from django.views.static import serve

from . import api, views

urlpatterns = []

# ------------------------------------------------------------------------------------
# ADMIN (including login/logout)
# ------------------------------------------------------------------------------------

if settings.ALLOW_ADMIN:
    admin.site.site_header = settings.SITE_TITLE
    admin.site.site_title = None
    admin.site.index_title = settings.SITE_TITLE
    admin.site.site_url = None  # remove "View Site" link
    urlpatterns.append(path("admin/", admin.site.urls))

# ------------------------------------------------------------------------------------
# STATIC / MEDIA (serve in develop mode)
# ------------------------------------------------------------------------------------

urlpatterns += (
    re_path(
        rf"^{settings.MEDIA_URL.strip('/')}(?P<path>.*)$",
        serve,
        {"document_root": settings.MEDIA_ROOT},
    ),
)

# also serve static files from collectstatic folder
# we want this to test if STATICFILES_STORAGE = ManifestStaticFilesStorage
# and we want to see if it automatically adds hashsum to {% static %}
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += (
    re_path(
        rf"^{settings.STATIC_URL.strip('/')}(?P<path>.*)$",
        serve,
        {"document_root": settings.STATIC_ROOT},
    ),
)


# ------------------------------------------------------------------------------------
#  REST API
#     NOTE: returns forbidden if no api url registered
# ------------------------------------------------------------------------------------


urlpatterns += [
    # include rest_api routes
    path("api/", include(api.api_router.urls)),
    # rest api doc from schema.json (generated with management command)
    path(
        "api.html",
        TemplateView.as_view(
            template_name="api/index.html",
            extra_context={"schema_url": static("api/schema.json")},
        ),
        name="api-doc",
    ),
]

# ------------------------------------------------------------------------------------
# MAIN APP: index
# ------------------------------------------------------------------------------------

urlpatterns += [
    path("", views.index_view),
    path("index.html", views.index_view, name="index"),
    path("_index.html", views._index_view, name="_index"),  # with login
]
