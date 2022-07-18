# coding: utf-8
import logging  # noqa

from django.conf import settings
from django.contrib.auth.decorators import login_required  # noqa
from django.shortcuts import render


def index(request):
    context = {"LANGUAGE_CODE": settings.LANGUAGE_CODE}
    return render(request, "main/index.html", context)


@login_required(login_url=None)
def _index(request):
    context = {"LANGUAGE_CODE": settings.LANGUAGE_CODE}
    return render(request, "main/index.html", context)
