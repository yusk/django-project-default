from unittest import mock
from datetime import datetime

from django.test import TestCase
from django.test.client import RequestFactory
from django.utils import timezone

from main.models import User
from main.views import AuthUUIDView, AuthUserViewWithEmail


class AuthUUIDViewTest(TestCase):
    def setUp(self):
        tz = timezone.get_current_timezone()
        dt = datetime(2021, 3, 4, 14, 57, 11, 703055)
        self.mock_date = tz.localize(dt)
        with mock.patch("django.utils.timezone.now") as mock_now:
            mock_now.return_value = self.mock_date
            self.user = User.objects.create_user(
                name="test_user",
                email="test@test.test",
                password="12345",
                device_uuid="7278cacb-f173-4ef9-b00f-bdbe68647c8d")

    def test_post(self):
        factory = RequestFactory()
        req = factory.post("/api/auth/uuid/",
                           {"uuid": "7278cacb-f173-4ef9-b00f-bdbe68647c8d"},
                           content_type="application/json")
        view = AuthUUIDView.as_view()
        res = view(req)
        self.assertEqual(res.status_code, 200)

    def test_post_not_exists_error(self):
        factory = RequestFactory()
        req = factory.post("/api/auth/uuid/",
                           {"uuid": "3fa85f64-5717-4562-b3fc-2c963f66afa6"},
                           content_type="application/json")
        view = AuthUUIDView.as_view()
        res = view(req)
        data = res.data
        self.assertEqual(res.status_code, 400)
        self.assertEqual(str(data["detail"]), "そのユーザーは存在しません")


class AuthUserViewWithEmailTest(TestCase):
    def setUp(self):
        tz = timezone.get_current_timezone()
        dt = datetime(2021, 3, 4, 14, 57, 11, 703055)
        self.mock_date = tz.localize(dt)
        with mock.patch("django.utils.timezone.now") as mock_now:
            mock_now.return_value = self.mock_date
            self.user = User.objects.create_user(name="user1",
                                                 email="user1@test.test",
                                                 password="user1",
                                                 email_confirmed=True)

    def test_post(self):
        factory = RequestFactory()
        req = factory.post("/api/auth/user/", {
            "email": "user1@test.test",
            "password": "user1"
        },
                           content_type="application/json")
        view = AuthUserViewWithEmail.as_view()
        res = view(req)
        self.assertEqual(res.status_code, 200)

    def test_post_email_confirmed_error(self):
        self.user.email_confirmed = False
        self.user.save()
        factory = RequestFactory()
        req = factory.post("/api/auth/user/", {
            "email": "user1@test.test",
            "password": "user1"
        },
                           content_type="application/json")
        view = AuthUserViewWithEmail.as_view()
        res = view(req)
        data = res.data
        self.assertEqual(res.status_code, 400)
        self.assertEqual(str(data["message"]), "先にメール確認を完了させてください。")
