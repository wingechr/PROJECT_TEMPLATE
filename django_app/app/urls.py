from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import include, path, re_path
from django.views.static import serve
from drf_spectacular.renderers import OpenApiJsonRenderer
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# from main.api import api_router
from main.views import InfoAPIView, index, profile, registration
from rest_framework.authtoken.views import obtain_auth_token

__all__ = ["urlpatterns"]

urlpatterns = []

# ------------------------------------------------------------------------------------
#  AUTH / ACOOUNTS
# ------------------------------------------------------------------------------------


urlpatterns += [
    # path("accounts/", include("django.contrib.auth.urls")),
    #  manually: # from django.contrib.auth import views as auth_views
    # show and handle login (GET/POST), default template accounts/login.html
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(template_name=None),
        name="logout",
    ),
    path(
        "accounts/profile/",
        profile,
        name="profile",
    ),
]

if settings.ALLOW_PASSWORD_RESET:
    urlpatterns += [
        path(
            "accounts/password_reset/",
            auth_views.PasswordResetView.as_view(
                template_name="accounts/password_reset_form.html",
                email_template_name="accounts/password_reset_email.html",
                subject_template_name="accounts/password_reset_subject.txt",
            ),
            name="password_reset",
        ),
        path(
            "accounts/password_reset/done/",
            auth_views.PasswordResetDoneView.as_view(
                template_name="accounts/password_reset_done.html"
            ),
            name="password_reset_done",
        ),
        path(
            "accounts/reset/<uidb64>/<token>/",
            auth_views.PasswordResetConfirmView.as_view(
                template_name="accounts/password_reset_confirm.html"
            ),
            name="password_reset_confirm",
        ),
        path(
            "accounts/reset/done/",
            auth_views.PasswordResetCompleteView.as_view(
                template_name="accounts/password_reset_complete.html"
            ),
            name="password_reset_complete",
        ),
    ]

if settings.ALLOW_REGISTER:
    urlpatterns += [
        path(
            "accounts/registration/",
            registration,
            name="registration",
        ),
    ]


# ------------------------------------------------------------------------------------
# ADMIN
# ------------------------------------------------------------------------------------

urlpatterns += [path("admin/", admin.site.urls)]

# ------------------------------------------------------------------------------------
# MEDIA (serve NOT from apache so we can add authentication )
# ------------------------------------------------------------------------------------

# Currently, we dont have media
# urlpatterns += [
#    re_path(f"{settings.MEDIA_URL.strip('/')}(?P<path>.*)$", views.media, name="media")
# ]

# ------------------------------------------------------------------------------------
# STATIC
#
# normally in production, this is handled by apacheand locallyin develop by django.
# BUT if we want to test it locally without debug and with offline compression,
# we need to serve it explicitly
# NOTE: if you do this, remember to run compress and collectstatic
#
# ------------------------------------------------------------------------------------
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
    path("api/", include("main.api"), name="api"),
    path("api/info/", InfoAPIView.as_view(), name="api-info"),
    path("api/login/", obtain_auth_token, name="api-login"),
    path(
        "api/schema/schema.json",
        login_required(
            SpectacularAPIView.as_view(renderer_classes=[OpenApiJsonRenderer])
        ),
        name="schema",  # must be named schema
    ),
    path(
        "api/schema/",
        login_required(SpectacularSwaggerView.as_view(url_name="schema")),
        # SpectacularRedocView.as_view(url_name="schema"),
        name="api-schema-ui",
    ),
]


# ------------------------------------------------------------------------------------
# MAIN APP (other)
# ------------------------------------------------------------------------------------


urlpatterns += [path("", index, name="index")]


# ------------------------------------------------------------------------------------
# DATA APP
# ------------------------------------------------------------------------------------

urlpatterns += [path("api/data/", include("data.api"))]
