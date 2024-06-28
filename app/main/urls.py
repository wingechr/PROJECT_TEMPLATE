from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.templatetags.static import static as static_path
from django.urls import include, path
from django.views.generic import TemplateView

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
# STATIC / MEDIA
# ------------------------------------------------------------------------------------

if settings.DEBUG:  # also serve static files from media
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()


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
            extra_context={"schema_url": static_path("api/restapi-schema.json")},
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
