# from django.urls import path, include

from django.db import connections
from django.db.migrations.recorder import MigrationRecorder
from django.http import JsonResponse
from main import __version__
from main.models import UserData
from rest_framework import permissions, routers, serializers, viewsets

from python_package import get_info

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
    # queryset = UserData.objects.all()
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


class InfoViewSet(viewsets.ViewSet):
    """
    System info
    """

    # Function to get the current migration revision ID
    @staticmethod
    def _get_current_migration_revision_id(app_name):
        connection = connections["default"]
        recorder = MigrationRecorder(connection)
        latest_migration = (
            recorder.migration_qs.filter(app=app_name).order_by("-applied").first()
        )
        if latest_migration:
            return latest_migration.name
        return None

    def list(self, request) -> dict:
        # TODO: how to tell python manage.py generateschema the output schema?
        data = get_info()
        data["version:app"] = __version__
        data["version:dbschema:main"] = self._get_current_migration_revision_id("main")

        return JsonResponse(data)


api_router.register("info", InfoViewSet, basename="api-info")
