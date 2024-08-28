# from django.shortcuts import render
# from django.contrib.auth import logout
# from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.template import loader

from .forms import UpdateUserForm


@login_required()  # login_url="accounts/login/"
def profile(request: HttpRequest):
    template = loader.get_template("main/profile.html")

    if request.method == "POST":
        user_form = UpdateUserForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Your profile is updated successfully")
            return redirect(to="profile")
    else:
        user_form = UpdateUserForm(instance=request.user)

    context = {"user_form": user_form}

    return HttpResponse(template.render(context, request))


def index(request: HttpRequest):
    # return HttpResponse("Hello, world. You're at the polls index.")
    template = loader.get_template("main/index.html")
    context = {}
    return HttpResponse(template.render(context, request))
