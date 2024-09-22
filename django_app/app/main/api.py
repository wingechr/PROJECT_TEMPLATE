# from django.urls import path, include

import django_filters
from django.db import IntegrityError
from django.http import JsonResponse
from drf_spectacular.openapi import AutoSchema
from main.models import Dataset, Upload, UserSetting
from main.utils import get_info
from rest_framework import (
    exceptions,
    generics,
    permissions,
    routers,
    serializers,
    viewsets,
)
from rest_framework.permissions import SAFE_METHODS, BasePermission


class ReadOnlyOrAuthenticated(BasePermission):
    """
    Custom permission to only allow authenticated users to perform write operations.
    Read operations are allowed for any request.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated


api_router = routers.DefaultRouter()


class UserSettingPermission(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class UserSettingFilter(django_filters.FilterSet):
    class Meta:
        model = UserSetting
        # field and allowed operators
        fields = {"key": ["exact"]}


class UserSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSetting
        # must either specify `fields` or `exclude`
        fields = ["key", "value", "timestamp", "id"]
        # exlude = []
        read_only_fields = ["timestamp", "id"]


class UserSettingModelViewSet(viewsets.ModelViewSet):
    # needed for api doc createtion, will be filtered in get_queryset
    queryset = UserSetting.objects.all()

    serializer_class = UserSettingSerializer
    permission_classes = [permissions.IsAuthenticated, UserSettingPermission]
    filterset_class = UserSettingFilter

    def get_queryset(self):
        # Ensure users can only see their own objects
        return UserSetting.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # save current user in field user
        serializer.save(user=self.request.user)


api_router.register("usersetting", UserSettingModelViewSet, basename="api-usersetting")


class BulkCreateListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        model = self.child.Meta.model

        # do NOT use model.create() because auto field will not be populated correctly
        # becaus we want to create bulk
        result = [model(**attrs) for attrs in validated_data]

        try:
            model.objects.bulk_create(result)
        except IntegrityError as e:
            raise exceptions.ValidationError(e)

        return result


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        # must either specify `fields` or `exclude`
        fields = ["key", "value", "id", "upload"]
        # fields = ["key", "value", "timestamp", "id", "upload"]
        read_only_fields = ["id"]
        list_serializer_class = BulkCreateListSerializer


class DatasetApiView(generics.ListCreateAPIView):

    permission_classes = [ReadOnlyOrAuthenticated]
    serializer_class = DatasetSerializer
    queryset = Dataset.objects.all()

    def get_serializer(self, *args, **kwargs):
        # if POST
        if not self.request.method == "GET":
            kwargs["many"] = True

            if not isinstance(kwargs.get("data", []), list):
                raise exceptions.ValidationError("data must be list")

            # create new upload items
            upload = Upload(user=self.request.user)
            upload.save()

            upload_id = upload.id
            for item in kwargs["data"]:
                item["upload"] = upload_id

        return super().get_serializer(*args, **kwargs)


# CUSTOM API ENDPOINTS


class FunctionApiSchema(AutoSchema):
    def get_operation(self, *args, **kwargs):
        result = super().get_operation(*args, **kwargs)
        result["responses"]["200"] = {
            "content": {"application/json": {"schema": {"type": "object"}}},
            "description": "",
        }
        return result


class MySerializer(serializers.BaseSerializer):
    fields = {}


class TestViewSet(viewsets.GenericViewSet):
    schema = FunctionApiSchema()
    serializer_class = MySerializer

    def list(self, response):
        "some description"
        return JsonResponse(get_info(), safe=False)


api_router.register("utils", TestViewSet, basename="api-utils")
