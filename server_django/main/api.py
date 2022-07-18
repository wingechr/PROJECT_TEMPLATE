# from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import serializers, viewsets

from .models import Example


# Serializers define the API representation.
class ExampleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Example
        # fields = []
        exclude = []


# ViewSets define the view behavior.
class ExampleViewSet(viewsets.ModelViewSet):
    queryset = Example.objects.all()
    serializer_class = ExampleSerializer


# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = []
        exclude = []


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


routes = [("main/example", ExampleViewSet), ("auth/user", UserViewSet)]
