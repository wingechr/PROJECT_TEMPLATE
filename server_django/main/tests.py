# coding: utf-8
import logging  # noqa

from django.contrib.auth.models import User
from django.db import models  # noqa
from django.db.utils import IntegrityError  # noqa
from django.forms import ValidationError  # noqa
from django.test import TestCase
from rest_framework.test import APIClient


class ModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="creator", is_superuser=True, is_active=True
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.user2 = User.objects.create(
            username="editor", is_staff=True, is_active=True
        )
        self.client2 = APIClient()
        self.client2.force_authenticate(user=self.user2)

    def test_1(self):
        pass
