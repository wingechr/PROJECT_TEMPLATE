import os
from tempfile import NamedTemporaryFile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from html5validator import Validator
from rest_framework.test import APIClient


class TestBaseAuth(TestCase):
    def setUp(self):
        call_command("create_default_users")
        # users created by create_default_users
        User = get_user_model()
        self.user_superuser = User.objects.get(email=settings.ADMIN_EMAIL)
        self.user_regular = User.objects.get(email=settings.TESTUSER_MAIL)

        self.client_superuser = APIClient()
        # self.client_superuser.force_authenticate(user=self.user_superuser)
        self.client_superuser.force_login(user=self.user_superuser)

        self.client_regular = APIClient()
        # self.client_regular.force_authenticate(user=self.user_regular)
        self.client_regular.force_login(user=self.user_regular)

        self.client_anonymous = APIClient()
        # self.request_factory = APIRequestFactory()


class TestPageAuth(TestBaseAuth):

    def test_authenticate(self):
        url_staff = reverse("admin:index")
        # staff/admin user can admin page
        res = self.client_superuser.get(url_staff)
        self.assertEqual(res.status_code, 200, res.content)

        # regular and anonylous user can NOT admin page
        res = self.client_regular.get(url_staff)
        self.assertEqual(res.status_code, 302, res.content)  # 302: redirect to login
        res = self.client_anonymous.get(url_staff)
        self.assertEqual(res.status_code, 302, res.content)  # 302: redirect to login
        self.assertTrue("login" in res.url, res.url)

        url_w_login = reverse("index")
        # authorized user can admin page
        res = self.client_regular.get(url_w_login)
        self.assertEqual(res.status_code, 200, res.content)

        # anonylous user can NOT admin page
        res = self.client_anonymous.get(url_w_login)
        self.assertEqual(res.status_code, 302, res.content)  # 302: redirect to login
        self.assertTrue("login" in res.url, res.url)


class ValidateHtml(TestBaseAuth):
    """NOTE: when using htmx, validation fails
    (Attribute "hx-get" not allowed on element "div" at this point)
    """

    def setUp(self):
        super().setUp()
        self.validator = Validator(
            ignore=[],
            ignore_re=[],
            errors_only=False,
            detect_language=False,
        )

    def test_index(self):

        url = reverse("index")
        res = self.client_regular.get(url)
        self.assertEqual(res.status_code, 200)

        # TODO: html5validator only can do files, can I do this without temp files?
        tmpfile = NamedTemporaryFile(
            "wb", suffix=".html", delete=False
        )  # must delete manually
        tmpfile.write(res.content)
        tmpfile.close()

        rc = self.validator.validate([tmpfile.name])

        os.remove(tmpfile.name)

        if rc:
            raise Exception()
