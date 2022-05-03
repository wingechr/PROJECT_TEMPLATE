# coding: utf-8
import logging  # noqa

from project.tools import get_api_create_url, get_api_details_url, register_model
from rest_framework import status
from rest_framework.test import APIClient

from django.contrib.auth.models import User
from django.db import models
from django.db.utils import IntegrityError  # noqa
from django.forms import ValidationError  # noqa
from django.test import TestCase


class Test(models.Model):
    name = models.CharField(max_length=10)
    user_create = models.ForeignKey(
        "auth.User",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="test_user_create",
        editable=False,
    )
    user_modified = models.ForeignKey(
        "auth.User",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="test_user_modified",
        editable=False,
    )


register_model(
    Test,
    excluded_fields=["user_create", "user_modified"],
    user_create_field="user_create",
    user_modified_field="user_modified",
    show_in_admin=False,
    show_in_api=True,
)


class ModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="creator")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.user2 = User.objects.create(username="editor")
        self.client2 = APIClient()
        self.client2.force_authenticate(user=self.user2)

    def test_api(self):
        # create
        url = get_api_create_url(Test)
        data = {"name": "Test 1"}
        res = self.client.post(path=url, data=data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # check user
        test1 = Test.objects.get(name="Test 1")
        self.assertEqual(test1.user_create, self.user)
        # modify
        url = get_api_details_url(Test, pk=test1.id)
        data = {"name": "Test 2"}
        res = self.client2.patch(path=url, data=data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test2 = Test.objects.get(id=test1.id)
        self.assertEqual(test2.user_create, self.user)
        self.assertEqual(test2.user_modified, self.user2)
        res = self.client.delete(path=url, data=data)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
