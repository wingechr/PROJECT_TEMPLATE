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
        self.assertEqual(res.status_code, 200, res)

        # authorized user can access _index.html
        res = self.client_staff.get(reverse("_index"))
        self.assertEqual(res.status_code, 200, res)

        # anonylous user can NOT access _index.html
        res = self.client_anonymous.get(reverse("_index"))
        self.assertEqual(res.status_code, 302, res)  # 302: redirect to login
        self.assertTrue("login" in res.url)

    def test_api_user_settings(self):
        url_list = reverse("api-usersetting-list")

        # authenticated user can add object
        res = self.client_staff.post(
            url_list, data={"key": "key1", "value": 10}, format="json"
        )
        self.assertEqual(res.status_code, 201, res)

        # change object
        id1 = res.json()["id"]
        url_id1 = reverse("api-usersetting-detail", args=[id1])

        # update
        res = self.client_staff.patch(url_id1, data={"value": 11})
        self.assertEqual(res.status_code, 200, res)

        # retrieve
        res = self.client_staff.get(url_id1)
        self.assertEqual(res.status_code, 200, res)
        self.assertEqual(res.json()["key"], "key1")
        self.assertEqual(res.json()["value"], 11)

        # filter
        self.client_staff.post(
            url_list, data={"key": "key2", "value": 20}, format="json"
        )
        res = self.client_staff.get(url_list)
        # make sure we have 2 datapoints
        self.assertEqual(res.status_code, 200, res)
        self.assertEqual(len(res.json()), 2)
        # filter by key
        res = self.client_staff.get(url_list, {"key": "key2"})
        self.assertEqual(res.status_code, 200, res)
        self.assertEqual(len(res.json()), 1)

        # different user cannot see/change other others items
        res = self.client_superuser.get(url_list)
        self.assertEqual(res.status_code, 200, res)
        self.assertEqual(res.json(), [])
        res = self.client_superuser.delete(url_id1)
        self.assertEqual(res.status_code, 404, res)

        # but owner can delete
        res = self.client_staff.delete(url_id1)
        self.assertEqual(res.status_code, 204, res)

        # anonymous user cannot read or write
        res = self.client_anonymous.post(
            url_list, data={"key": "key2", "value": "value2"}, format="json"
        )
        self.assertEqual(res.status_code, 401, res)
        res = self.client_anonymous.get(url_list)
        self.assertEqual(res.status_code, 401, res)

    def test_api_dataset(self):
        url_list = reverse("api-dataset")

        # authenticated user can bulk create
        res = self.client_staff.post(
            url_list,
            data=[{"key": "key1", "value": 10}, {"key": "key2", "value": 20}],
            format="json",  # must be json
        )
        self.assertEqual(res.status_code, 201, res)
        res = self.client_staff.get(url_list)
        self.assertEqual(res.status_code, 200, res)
        self.assertEqual(len(res.json()), 2)

        # another authenticated user can create data with partial overlap of keys
        res = self.client_superuser.post(
            url_list,
            data=[{"key": "key1", "value": 11}, {"key": "key3", "value": 30}],
            format="json",  # must be json
        )
        self.assertEqual(res.status_code, 201, res)
        res = self.client_superuser.get(url_list)
        self.assertEqual(res.status_code, 200, res)
        self.assertEqual(len(res.json()), 4)

        # anonymous user can read but not write
        res = self.client_anonymous.get(url_list)
        self.assertEqual(res.status_code, 200, res)
        self.assertEqual(len(res.json()), 4)

        res = self.client_anonymous.post(url_list, data={})
        self.assertEqual(res.status_code, 401, res)
