# coding: utf-8
import logging  # noqa

from django.conf import settings
from django.contrib import admin
from django.db import models  # noqa
from django.db.models.query_utils import DeferredAttribute
from django.forms import ValidationError
from django.urls import include, path, re_path, reverse  # noqa
from rest_framework import generics, permissions, serializers
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.views import Response, status

# TODO https://docs.djangoproject.com/en/2.1/ref/models/instances/#get-absolute-url


API_PERMISSION_CLASSES = [permissions.IsAuthenticated]
API_RENDERER_CLASSES = [JSONRenderer]
if settings.ALLOW_BROWSER_API:
    API_RENDERER_CLASSES.append(BrowsableAPIRenderer)


def is_field(attr):
    return isinstance(attr, DeferredAttribute)


def get_api_create_url_name(cls):
    model_name = cls.__name__.lower()
    return "api_%s_create" % (model_name,)


def get_api_details_url_name(cls):
    model_name = cls.__name__.lower()
    return "api_%s_details" % (model_name,)


def get_api_create_url(cls, **kwargs):
    return reverse(get_api_create_url_name(cls), kwargs=kwargs)


def get_api_details_url(cls, **kwargs):
    return reverse(get_api_details_url_name(cls), kwargs=kwargs)


def register_model(
    mod,
    name=None,
    order_fields=None,
    show_readonly_fields=None,
    excluded_fields=None,
    filter_fields=None,
    user_create_field=None,
    user_modified_field=None,
    show_in_admin=False,
    show_in_api=False,
    filter_items=None,
):

    if show_in_admin:

        class ModelAdmin(admin.ModelAdmin):
            filter_horizontal = filter_fields or []
            readonly_fields = show_readonly_fields if show_readonly_fields else []

            def get_ordering(self, request):
                fields = ["id"]
                if order_fields:
                    fields = list(order_fields) + fields
                return fields

            def save_model(self, request, obj, form, change):
                if user_modified_field:
                    setattr(obj, user_modified_field, request.user)
                if not change and user_create_field:
                    setattr(obj, user_create_field, request.user)
                super().save_model(request, obj, form, change)

            def get_queryset(self, request):
                qs = super().get_queryset(request)
                if filter_items:
                    qs = filter_items(qs)
                return qs

        admin.site.register(mod, ModelAdmin)

    if show_in_api:
        excluded_fields = set(excluded_fields or [])
        excluded_fields = excluded_fields | set(f + "_id" for f in excluded_fields)
        serialized_fields = [
            fn
            for fn, f in mod.__dict__.items()
            if is_field(f) and fn not in excluded_fields
        ]
        serialized_fields = [
            f[:-3] if f.endswith("_id") else f for f in serialized_fields
        ]  # *_id --> *

        if name:
            model_name = name
        else:
            model_name = mod.__name__.lower()

        class ModelSerializer(serializers.ModelSerializer):
            class Meta:
                model = mod
                fields = serialized_fields

        class ListCreateAPIView(generics.ListCreateAPIView):
            queryset = mod.objects.all()
            serializer_class = ModelSerializer
            renderer_classes = API_RENDERER_CLASSES
            permission_classes = API_PERMISSION_CLASSES

            def perform_create(self, serializer):
                kwargs = {}
                if user_create_field:
                    kwargs[user_create_field] = self.request.user
                if user_modified_field:
                    kwargs[user_modified_field] = self.request.user
                serializer.save(**kwargs)

            def create(self, *args, **kwargs):
                # request = args[0]
                try:
                    return super().create(*args, **kwargs)
                except ValidationError as e:
                    content = {"ValidationError": "\n".join(e.messages)}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)

        class RetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
            queryset = mod.objects.all()
            serializer_class = ModelSerializer
            renderer_classes = API_RENDERER_CLASSES
            permission_classes = API_PERMISSION_CLASSES

            def perform_update(self, serializer, *args, **kwargs):
                kwargs = {}
                if user_modified_field:
                    kwargs[user_modified_field] = self.request.user
                serializer.save(**kwargs)

            def update(self, *args, **kwargs):
                try:
                    return super().update(*args, **kwargs)
                except ValidationError as e:
                    content = {"ValidationError": "\n".join(e.messages)}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)

        from main.urls import urlpatterns  # must be in an app, not in project

        urlpatterns.append(
            path(
                "api/%s/" % model_name,
                ListCreateAPIView.as_view(),
                name=get_api_create_url_name(mod),
            )
        )
        urlpatterns.append(
            re_path(
                "api/%s/(?P<pk>[0-9]+)/$" % model_name,
                RetrieveUpdateDestroyAPIView.as_view(),
                name=get_api_details_url_name(mod),
            )
        )
