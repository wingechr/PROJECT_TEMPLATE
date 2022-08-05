# from django.urls import path, include
from django.http import JsonResponse  # noqa
from main.settings import BASE_URL
from rest_framework import serializers, viewsets  # noqa
from rest_framework.schemas import coreapi

from . import models  # noqa


class ApiSchema(coreapi.AutoSchema):
    """create schema js for client"""

    def get_link(self, path, method, base_url):
        return super().get_link(path, method, BASE_URL)


"""
class ExampleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Example
        # fields = []
        exclude = []


# ViewSets define the view behavior.
class ExampleModelViewSet(viewsets.ModelViewSet):
    queryset = models.Example.objects.all()
    serializer_class = ExampleModelSerializer

class DummyViewset(viewsets.ViewSet):
    def list(self, request):  # GET on instance root
        return JsonResponse([{"id": 1}], safe=False)

"""

routes = [
    # ("main/example", ExampleModelViewSet),
    # ("main/dummy", DummyViewset, "dummy")
]
