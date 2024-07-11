# from django.urls import path, include


from django.http import JsonResponse
from drf_spectacular.openapi import AutoSchema
from main.models import UserData
from main.utils import get_info
from rest_framework import permissions, routers, serializers, viewsets

api_router = routers.DefaultRouter()


class UserDataPermission(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        # must either specify `fields` or `exclude`
        fields = ["key", "value", "created_at", "id"]
        exlude = ["created_by"]
        # read_only_fields = []


class UserDataModelViewSet(viewsets.ModelViewSet):
    queryset = UserData.objects.all()
    serializer_class = UserDataSerializer
    permission_classes = [permissions.IsAuthenticated, UserDataPermission]

    def get_queryset(self):
        # Ensure users can only see their own objects
        return UserData.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        # save current user in field created_by
        serializer.save(created_by=self.request.user)


# basename is importtant for reverse url lookup
api_router.register("userdata", UserDataModelViewSet, basename="api-userdata")


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
