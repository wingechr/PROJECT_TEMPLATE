from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http.request import HttpRequest
from django.shortcuts import HttpResponse, redirect, render
from drf_spectacular.utils import extend_schema, inline_serializer
from main import __version__
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import RegistrationForm, UserPasswordChangeForm, UserProfileForm


def registration(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")  # Redirect to a success page
        else:
            for key, val in form.errors:
                messages.error(request, f"{key}: {val}")
    else:
        form = RegistrationForm()

    return render(
        request,
        template_name="accounts/registration.html",
        context={"form": form},
    )


@login_required()
def profile(request: HttpRequest) -> HttpResponse:
    user = request.user
    # NOTE: user data and password should be handled in separate forms

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user)
        form_passwd = UserPasswordChangeForm(request.user, request.POST)

        # check if user entererd anything in new password fields
        password_changed = any(
            request.POST.get(fld)
            for fld in [
                # "old_password", # this is sometimes auto filled by browser
                "new_password1",
                "new_password2",
            ]
        )

        if form.is_valid() and (form_passwd.is_valid() or not password_changed):
            user = form.save()
            if password_changed:
                form_passwd.save()
                update_session_auth_hash(
                    request, form_passwd.user
                )  # Keeps the user logged in
            messages.success(request, "Profile updated successfully!")
        else:
            for key, val in form.errors:
                messages.error(request, f"{key}: {val}")
            if password_changed:
                for key, val in form_passwd.errors:
                    messages.error(request, f"{key}: {val}")
        # Redirect to the same URL to to a GET,
        # so reloading of page does not repeat operation
        return redirect(request.path)

    else:
        form = UserProfileForm(instance=user)
        form_passwd = UserPasswordChangeForm(request.user)

    return render(
        request,
        template_name="accounts/profile.html",
        context={
            "form": form,
            "form_passwd": form_passwd,
        },
    )


@login_required()
def index(request: HttpRequest) -> HttpResponse:
    return render(request, template_name="main/index.html")


class InfoAPIView(APIView):
    @extend_schema(
        responses={
            200: inline_serializer(
                name="CustomData",
                fields={"version": serializers.CharField()},
                many=False,
            )
        },
        description="system information",
        tags=["api"],  # otherwise its in group "default"
    )
    def get(self, request):
        data = {"version": __version__}
        return Response(data)
