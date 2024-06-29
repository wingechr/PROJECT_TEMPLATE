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
        url_list = reverse("api-userdata-list")

        # authenticated user can add object
        res = self.client_staff.post(url_list, data={"key": "key1", "value": "value1a"})
        self.assertEqual(res.status_code, 201)

        # change object
        id1 = res.json()["id"]
        url_id1 = reverse("api-userdata-detail", args=[id1])

        # update
        res = self.client_staff.patch(url_id1, data={"value": "value1b"})
        self.assertEqual(res.status_code, 200)

        # retrieve
        res = self.client_staff.get(url_id1)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["key"], "key1")
        self.assertEqual(res.json()["value"], "value1b")

        # different user cannot see/change other others items
        res = self.client_superuser.get(url_list)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), [])
        res = self.client_superuser.delete(url_id1)
        self.assertEqual(res.status_code, 404)

        # but owner can delete
        res = self.client_staff.delete(url_id1)
        self.assertEqual(res.status_code, 204)

        # anonymoususer cannot read or write
        res = self.client_anonymous.post(
            url_list, data={"key": "key2", "value": "value2"}
        )
        self.assertEqual(res.status_code, 401)
        res = self.client_anonymous.get(url_list)
        self.assertEqual(res.status_code, 401)
