from unittest import mock
from datetime import datetime

from django.test import TestCase
from django.test.client import RequestFactory
from django.utils import timezone
from rest_framework.test import force_authenticate

from main.models import User
from main.views import UserPasswordView


class UserPasswordViewTest(TestCase):
    def setUp(self):
        tz = timezone.get_current_timezone()
        dt = datetime(2021, 3, 4, 14, 57, 11, 703055)
        self.mock_date = tz.localize(dt)
        with mock.patch("django.utils.timezone.now") as mock_now:
            mock_now.return_value = self.mock_date
            self.user = User.objects.create_user(name="test_user",
                                                 email="test@test.test",
                                                 password="password")

    def test_put_user_password(self):
        factory = RequestFactory()
        req = factory.put("/api/user/password", {
            "password": "password",
            "new_password": "newPassWord",
            "new_password_confirm": "newPassWord",
        }, content_type="application/json")
        force_authenticate(req, user=self.user)
        view = UserPasswordView.as_view()
        res = view(req)
        self.assertEqual(res.status_code, 200)

    def test_put_user_password_not_matched_error(self):
        factory = RequestFactory()
        req = factory.put("/api/user/password", {
            "password": "12345678",
            "new_password": "newPassWord",
            "new_password_confirm": "newPassWord",
        }, content_type="application/json")
        force_authenticate(req, user=self.user)
        view = UserPasswordView.as_view()
        res = view(req)
        data = res.data
        self.assertEqual(res.status_code, 400)
        self.assertEqual(str(data["password"]), "password not matched")
