# from django.urls import path, include


from django.db import connections
from django.db.migrations.recorder import MigrationRecorder
from django.http import JsonResponse
from main import settings
from main.models import Version
from rest_framework import routers, serializers, viewsets

from python_package import get_info

api_router = routers.DefaultRouter()


class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        # must either specify `fields` or `exclude`
        fields = ["version", "created_at"]
        exlude = ["created_by"]
        # read_only_fields = []


class VersionModelViewSet(viewsets.ModelViewSet):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer

    def perform_create(self, serializer):
        # save current user in field created_by
        serializer.save(created_by=self.request.user)


# basename is importtant for reverse url lookup
api_router.register("version", VersionModelViewSet, basename="api-version")


# CUSTOM API ENDPOINTS


# Function to get the current migration revision ID
def get_current_migration_revision_id(app_name):
    connection = connections["default"]
    recorder = MigrationRecorder(connection)
    latest_migration = (
        recorder.migration_qs.filter(app=app_name).order_by("-applied").first()
    )
    if latest_migration:
        return latest_migration.name
    return None


class ExampleViewSet(viewsets.ViewSet):
    """
    A simple example Viewset with only GET method
    """

    def list(self, request):
        data = get_info()
        data["version:python_package"] = data.pop("version")
        data["version:app"] = settings.__version__
        data["version:db_schema:main"] = get_current_migration_revision_id("main")

        return JsonResponse(data)


api_router.register("example", ExampleViewSet, basename="api-example")
