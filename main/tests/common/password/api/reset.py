from unittest import mock
from datetime import datetime

from django.test import TestCase
from django.core import mail
from django.test.client import RequestFactory
from django.utils import timezone

from main.models import User, PasswordResetToken
from main.views import PasswordResetView


class PasswordResetViewTest(TestCase):
    def setUp(self):
        self.tz = timezone.get_current_timezone()
        dt = datetime(2021, 3, 4, 14, 57, 11, 703055)
        self.mock_date = self.tz.localize(dt)
        with mock.patch("django.utils.timezone.now") as mock_now:
            mock_now.return_value = self.mock_date
            self.user = User.objects.create_user(name="test_user",
                                                 email="test@test.test",
                                                 password="password")
            self.prt = PasswordResetToken.update_or_create(user=self.user)

    def test_post(self):
        factory = RequestFactory()
        req = factory.post(
            "/api/password/", {
                "token": self.prt.token,
                "password": "newPassword",
                "password_confirm": "newPassword"
            })
        view = PasswordResetView.as_view()
        res = view(req)
        data = res.data
        self.assertEqual(res.status_code, 200)
        self.assertEqual(str(data["message"]), "パスワードの変更が完了しました。")
        self.assertEqual(
            PasswordResetToken.objects.filter(user=self.user).count(), 0)

    def test_post_expired_error(self):
        expired_at = datetime(2021, 3, 4, 14, 57, 11, 703055)
        self.prt.expired_at = self.tz.localize(expired_at)
        self.prt.save()
        factory = RequestFactory()
        req = factory.post(
            "/api/password/", {
                "token": self.prt.token,
                "password": "newPassword",
                "password_confirm": "newPassword"
            })
        view = PasswordResetView.as_view()
        res = view(req)
        data = res.data
        self.assertEqual(res.status_code, 400)
        self.assertEqual(str(data["message"]),
                         "パスワードリセットの有効期限が切れています。再度発行してください。")
        self.assertEqual(
            PasswordResetToken.objects.filter(user=self.user).count(), 1)

    def test_post_token_error(self):
        factory = RequestFactory()
        req = factory.post(
            "/api/password/", {
                "token": "string",
                "password": "password",
                "password_confirm": "password"
            })
        view = PasswordResetView.as_view()
        res = view(req)
        data = res.data
        self.assertEqual(res.status_code, 400)
        self.assertEqual(str(data["message"]), "パスワードリセットトークンが一致しませんでした。")
        self.assertEqual(len(mail.outbox), 0)

    def test_post_password_length_error(self):
        factory = RequestFactory()
        req = factory.post("/api/password/", {
            "token": "string",
            "password": "string",
            "password_confirm": "string"
        })
        view = PasswordResetView.as_view()
        res = view(req)
        data = res.data
        self.assertEqual(res.status_code, 400)
        self.assertEqual(str(data["password"][0]), "この項目は少なくとも8文字以上にしてください。")
        self.assertEqual(str(data["password_confirm"][0]),
                         "この項目は少なくとも8文字以上にしてください。")
        self.assertEqual(
            PasswordResetToken.objects.filter(user=self.user).count(), 1)

    def test_post_password_error(self):
        factory = RequestFactory()
        req = factory.post(
            "/api/password/", {
                "token": self.prt.token,
                "password": "newPassword",
                "password_confirm": "wrongPassword"
            })
        view = PasswordResetView.as_view()
        res = view(req)
        data = res.data
        self.assertEqual(res.status_code, 400)
        self.assertEqual(str(data["password"][0]), "パスワード確認がパスワードと一致していません。")
        self.assertEqual(
            PasswordResetToken.objects.filter(user=self.user).count(), 1)
