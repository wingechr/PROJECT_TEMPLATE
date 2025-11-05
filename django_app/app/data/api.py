from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status, viewsets
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter

from .models import Data

__all__ = ["urlpatterns"]


class DataFilter(filters.FilterSet):
    key = filters.CharFilter(field_name="key", lookup_expr="eq")

    class Meta:
        model = Data
        fields = ["key"]


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = "__all__"


class DataViewSet(
    # not full viewset: only list, get and create
    viewsets.GenericViewSet,
    viewsets.mixins.RetrieveModelMixin,
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.CreateModelMixin,
):
    queryset = Data.objects.all()
    serializer_class = DataSerializer
    filterset_class = DataFilter

    # request and response are multiple=True
    @extend_schema(
        request=DataSerializer(many=True), responses=DataSerializer(many=True)
    )
    def create(self, request):
        # create multiple
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


api_router = DefaultRouter()
api_router.register("data", DataViewSet, basename="api-data-data")

urlpatterns = api_router.urls  # for include in main urls
