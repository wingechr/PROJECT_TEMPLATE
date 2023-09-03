from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required  # noqa
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponseForbidden, JsonResponse
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


def get_schema_view_v2(request):
    return JsonResponse(
        {
            "openapi": "3.0.2",
            # "info": {"title": "", "version": ""},
            "paths": {
                "/api/v2/": {
                    "get": {
                        "operationId": "test_api_v2",
                        "description": "",
                        "parameters": [
                            {"in": "query", "name": "p1", "type": "integer"}
                        ],
                        "responses": {
                            "200": {
                                "content": {
                                    "application/json": {
                                        "schema": {"type": "array", "items": {}}
                                    }
                                },
                                "description": "",
                            }
                        },
                        "tags": ["api"],
                    }
                }
            },
        },
        safe=False,
    )


def test_api_v2(request):
    if request.user.is_anonymous:
        return HttpResponseForbidden()
    param = int(request.GET.get("p1") or "0")

    return JsonResponse([{"id": param + 1}], safe=False)


# NOTE: returns forbidden if no api url registered
urlpatterns += [
    path("api/v1/", include(api.api_router.urls)),
    path(
        "openapi.json",
        get_schema_view(renderer_classes=[JSONOpenAPIRenderer]),
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
    path("api/v2/", test_api_v2),
    path(
        "openapi2.json",
        get_schema_view_v2,
        name="openapi-schema2",
    ),
    path(
        "apidoc2/",
        TemplateView.as_view(
            template_name="main/apidoc.html",
            extra_context={"schema_url": "openapi-schema2"},
        ),
        name="apidoc2",
    ),
]

# MAIN APP

urlpatterns += [
    path("", views.index, name="index"),
]
