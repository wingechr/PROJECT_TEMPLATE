# from django.urls import path, include


from django.http import JsonResponse
from rest_framework import routers, serializers, viewsets

from app.models import Version

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


class ExampleViewSet(viewsets.ViewSet):
    """
    A simple example Viewset with only GET method
    """

    def list(self, request):
        return JsonResponse({})


api_router.register("example", ExampleViewSet, basename="api-example")
