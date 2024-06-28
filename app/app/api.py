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


def api_example_view(request):
    value = float(request.GET["value"])
    value = value + 1
    return JsonResponse({"value": value})
