from rest_framework import serializers, viewsets
from rest_framework.routers import DefaultRouter

from .models import Data

__all__ = ["urlpatterns"]


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = "__all__"


class DataViewSet(viewsets.ModelViewSet):
    queryset = Data.objects.all()
    serializer_class = DataSerializer


api_router = DefaultRouter()
api_router.register("data", DataViewSet, basename="api-data-data")

urlpatterns = api_router.urls  # for include in main urls
