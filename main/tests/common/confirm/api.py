from unittest import mock
from datetime import datetime

from django.test import TestCase
from django.core import mail
from django.test.client import RequestFactory
from django.utils import timezone

from main.models import User, AuthDigit
from main.views import ConfirmDigitView, ConfirmDigitResetView


class ConfirmDigitViewTest(TestCase):
    def setUp(self):
        self.tz = timezone.get_current_timezone()
        dt = datetime(2021, 3, 4, 14, 57, 11, 703055)
        self.mock_date = self.tz.localize(dt)
        with mock.patch("django.utils.timezone.now") as mock_now:
            mock_now.return_value = self.mock_date
            self.user = User.objects.create_user(name="test_user",
                                                 email="test@test.test",
                                                 password="12345")

    def test_post(self):
        auth = AuthDigit.objects.create(user=self.user)
        factory = RequestFactory()
        req = factory.post("/api/confirm/digit/", {"digit": auth.code})
        view = ConfirmDigitView.as_view()
        res = view(req)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(AuthDigit.objects.filter(user=self.user).count(), 0)
        self.assertTrue(User.objects.get(name="test_user").email_confirmed)

    def test_post_expired_error(self):
        auth = AuthDigit.objects.create(user=self.user,
                                        expired_at=self.mock_date)
        factory = RequestFactory()
        req = factory.post("/api/confirm/digit/", {"digit": auth.code})
        view = ConfirmDigitView.as_view()
        res = view(req)
        data = res.data
        self.assertEqual(res.status_code, 400)
        self.assertEqual(str(data["message"]), "確認コードの有効期限が切れています。再度発行してください。")
        self.assertEqual(AuthDigit.objects.filter(user=self.user).count(), 1)
        self.assertFalse(User.objects.get(name="test_user").email_confirmed)

    def test_post_auth_error(self):
        factory = RequestFactory()
        req = factory.post("/api/confirm/digit/", {"digit": "wrongCode"})
        view = ConfirmDigitView.as_view()
        res = view(req)
        data = res.data
        self.assertEqual(res.status_code, 400)
        self.assertEqual(str(data["message"]), "確認コードが一致しませんでした。")
        self.assertFalse(User.objects.get(name="test_user").email_confirmed)


class ConfirmDigitResetViewTest(TestCase):
    def setUp(self):
        tz = timezone.get_current_timezone()
        dt = datetime(2021, 3, 4, 14, 57, 11, 703055)
        self.mock_date = tz.localize(dt)
        with mock.patch("django.utils.timezone.now") as mock_now:
            mock_now.return_value = self.mock_date
            self.user = User.objects.create_user(name="test_user",
                                                 email="test@test.test",
                                                 password="12345")

    def test_post(self):
        factory = RequestFactory()
        req = factory.post("/api/confirm/digit/reset/",
                           {"email": "test@test.test"})
        view = ConfirmDigitResetView.as_view()
        res = view(req)
        data = res.data
        self.assertEqual(res.status_code, 200)
        self.assertEqual(str(data["message"]),
                         "メールアドレスに確認コードを再送信しました。コードを入力して登録を完了させてください。")
        self.assertEqual(AuthDigit.objects.filter(user=self.user).count(), 1)
        self.assertEqual(len(mail.outbox), 1)

    def test_post_user_error(self):
        factory = RequestFactory()
        req = factory.post("/api/confirm/digit/reset/",
                           {"email": "user@test.test"})
        view = ConfirmDigitResetView.as_view()
        res = view(req)
        data = res.data
        self.assertEqual(res.status_code, 400)
        self.assertEqual(str(data["message"]), "登録されたユーザーが見つかりませんでした。")
        self.assertEqual(AuthDigit.objects.filter(user=self.user).count(), 0)
        self.assertEqual(len(mail.outbox), 0)

    def test_post__too_many_email_request_error(self):
        AuthDigit.objects.create(user=self.user)
        factory = RequestFactory()
        req = factory.post("/api/confirm/digit/reset/",
                           {"email": "test@test.test"})
        view = ConfirmDigitResetView.as_view()
        res = view(req)
        data = res.data
        self.assertEqual(res.status_code, 400)
        self.assertEqual(str(data["message"]),
                         "メールは短時間に連続して送ることができません。お手数ですが時間を空けてからお試しください。")
        self.assertEqual(AuthDigit.objects.filter(user=self.user).count(), 1)
        self.assertEqual(len(mail.outbox), 0)
