from unittest import mock
from datetime import datetime

from django.test import TestCase
from django.test.client import RequestFactory
from django.utils import timezone
from rest_framework.test import force_authenticate

from main.models import User
from main.views import UserViewSet


class UserViewSetTest(TestCase):
    def setUp(self):
        tz = timezone.get_current_timezone()
        dt = datetime(2021, 3, 4, 14, 57, 11, 703055)
        self.mock_date = tz.localize(dt)
        with mock.patch("django.utils.timezone.now") as mock_now:
            mock_now.return_value = self.mock_date
            self.user1 = User.objects.create_user(name="user",
                                                  email="user@test.test",
                                                  password="12345")
            self.user2 = User.objects.create_user(name="test_user",
                                                  email="testuser@test.test",
                                                  password="54321")
            self.user3 = User.objects.create_user(name="tester",
                                                  email="tester@test.test",
                                                  password="password")

    def test_get_users(self):
        factory = RequestFactory()
        req = factory.get("/api/users/")
        view = UserViewSet.as_view({"get": "list"})
        force_authenticate(req, user=self.user1)
        res = view(req)
        data = res.data
        self.assertEqual(res.status_code, 200)
        self.assertSetEqual(set(data.keys()),
                            set(("count", "next", "previous", "results")))
        self.assertEquals(data["count"], 3)
        self.assertEqual(data["results"][0]["name"], "user")

    def test_get_user(self):
        factory = RequestFactory()
        req = factory.get(f"/api/users/{self.user1.id}")
        view = UserViewSet.as_view({"get": "retrieve"})
        force_authenticate(req, user=self.user1)
        res = view(req, pk=self.user1.id)
        data = res.data
        self.assertEqual(res.status_code, 200)
        self.assertSetEqual(set(data.keys()), set(("id", "name", "icon")))
        self.assertEqual(data["name"], "user")
