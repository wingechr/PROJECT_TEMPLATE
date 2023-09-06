from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient


class ModelTestCase(TestCase):
    def setUp(self):
        self.user_superuser = User.objects.create(
            username="superuser", is_superuser=True, is_active=True
        )
        self.client_superuser = APIClient()
        # self.client_superuser.force_authenticate(user=self.user_superuser)
        self.client_superuser.force_login(user=self.user_superuser)

        self.user_staff = User.objects.create(
            username="staff", is_staff=True, is_active=True
        )
        self.client_staff = APIClient()
        # self.client_staff.force_authenticate(user=self.user_staff)
        self.client_staff.force_login(user=self.user_staff)

        self.client_anonymous = APIClient()

    def test_authenticate(self):
        # anonylous user can access index.html
        res = self.client_anonymous.get(reverse("index"))
        self.assertEqual(res.status_code, 200)

        # authorized user can access _index.html
        res = self.client_staff.get(reverse("_index"))
        self.assertEqual(res.status_code, 200)

        # anonylous user can NOT access _index.html
        res = self.client_anonymous.get(reverse("_index"))
        self.assertEqual(res.status_code, 302)  # 302: redirect to login
        self.assertTrue("login" in res.url)

    def test_authenticate_api(self):
        url_list = reverse("api-version-list")
        url_v1 = reverse("api-version-detail", args=["v1"])

        # authenticated user can add object
        res = self.client_staff.post(url_list, data={"version": "v1"})
        # replace directly with put
        res = self.client_staff.put(url_v1, data={"version": "v1"})
        self.assertEqual(res.status_code, 200)

        # anonymoususer cannot add
        res = self.client_anonymous.post(url_list, data={"version": "v1"})
        self.assertEqual(res.status_code, 401)
        # ... but they can see existing items

        # list items is allowed for all
        res = self.client_anonymous.get(url_list)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()[0]["version"], "v1")

        res = self.client_anonymous.get(url_v1)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["version"], "v1")
        self.assertTrue("created_at" in res.json())
        self.assertFalse("created_by" in res.json())  # user should be hidden

        res = self.client_anonymous.delete(url_v1)
        self.assertEqual(res.status_code, 401)

        res = self.client_staff.delete(url_v1)
        self.assertEqual(res.status_code, 204)
