# from django.urls import path, include

from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse  # noqa
from rest_framework import routers, serializers, viewsets  # noqa

api_router = routers.DefaultRouter()


class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        #        # fields = []
        exclude = []


class ContentTypeModelViewSet(viewsets.ModelViewSet):
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer


class Simple(viewsets.ViewSet):
    def list(self, request):  # GET on instance root
        return JsonResponse([{"id": 1}], safe=False)


api_router.register("main/simple", Simple, basename="simple")
# api_router.register("main/content_type", ContentTypeModelViewSet)
