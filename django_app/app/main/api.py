from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter

User = get_user_model()

__all__ = ["urlpatterns"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "last_login",
            "date_joined",
            "email",
            "groups",
            "language",
            "is_superuser",
            "is_active",
            "is_staff",
        ]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()  # we need to limit it later, but need it for schema
    serializer_class = UserSerializer
    many = False

    def get_queryset(self):
        """IMPORTANT! only return current user"""
        queryset = self.queryset
        queryset = queryset.filter(pk=self.request.user.pk)
        return queryset

    @extend_schema(exclude=True)
    def retrieve(self, request, *args, **kwargs):
        return Response(status=405)  # Method Not Allowed

    @extend_schema(exclude=True)
    def create(self, request, *args, **kwargs):
        return Response(status=405)  # Method Not Allowed

    @extend_schema(exclude=True)
    def update(self, request, *args, **kwargs):
        return Response(status=405)  # Method Not Allowed

    @extend_schema(exclude=True)
    def partial_update(self, request, *args, **kwargs):
        return Response(status=405)  # Method Not Allowed

    @extend_schema(exclude=True)
    def destroy(self, request, *args, **kwargs):
        return Response(status=405)  # Method Not Allowed


api_router = DefaultRouter()
api_router.register("user", UserViewSet, basename="api-user")

urlpatterns = api_router.urls  # for include in main urls
