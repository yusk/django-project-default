from unittest import mock
from datetime import datetime

from django.test import TestCase
from django.test.client import RequestFactory
from django.utils import timezone

from main.models import User, AuthDigit, PasswordResetToken
from main.views import PasswordResetDigitView


class PasswordResetDigitViewTest(TestCase):
    def setUp(self):
        self.tz = timezone.get_current_timezone()
        dt = datetime(2021, 3, 4, 14, 57, 11, 703055)
        self.mock_date = self.tz.localize(dt)
        with mock.patch("django.utils.timezone.now") as mock_now:
            mock_now.return_value = self.mock_date
            self.user = User.objects.create_user(name="test_user",
                                                 email="test@test.test",
                                                 password="12345")
            self.auth = AuthDigit.update_or_create(user=self.user)

    def test_post(self):
        factory = RequestFactory()
        req = factory.post("/api/password/digit/", {
            "digit": self.auth.code
        })
        view = PasswordResetDigitView.as_view()
        res = view(req)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(AuthDigit.objects.filter(user=self.user).count(), 0)
        self.assertEqual(
            PasswordResetToken.objects.filter(user=self.user).count(), 1)

    def test_post_expired_error(self):
        expired_at = datetime(2021, 3, 3, 00, 00, 00, 000000)
        self.auth.expired_at = self.tz.localize(expired_at)
        self.auth.save()
        factory = RequestFactory()
        req = factory.post("/api/password/digit/", {
            "digit": self.auth.code
        })
        view = PasswordResetDigitView.as_view()
        res = view(req)
        data = res.data
        self.assertEqual(res.status_code, 400)
        self.assertEqual(str(data["message"]), "確認コードの有効期限が切れています。再度発行してください。")
        self.assertEqual(AuthDigit.objects.filter(user=self.user).count(), 1)
        self.assertEqual(
            PasswordResetToken.objects.filter(user=self.user).count(), 0)

    def test_post_auth_error(self):
        factory = RequestFactory()
        req = factory.post("/api/password/digit/", {
            "digit": "wrongCode"
        })
        view = PasswordResetDigitView.as_view()
        res = view(req)
        data = res.data
        self.assertEqual(res.status_code, 400)
        self.assertEqual(str(data["message"]), "確認コードが一致しませんでした。")
        self.assertEqual(AuthDigit.objects.filter(user=self.user).count(), 1)
        self.assertEqual(
            PasswordResetToken.objects.filter(user=self.user).count(), 0)
