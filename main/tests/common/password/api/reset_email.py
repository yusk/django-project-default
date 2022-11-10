from unittest import mock
from datetime import datetime

from django.test import TestCase
from django.core import mail
from django.test.client import RequestFactory
from django.utils import timezone

from main.models import User, AuthDigit
from main.views import PasswordResetEmailView


class PasswordResetEmailViewTest(TestCase):
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
        req = factory.post("/api/password/email/", {"email": "test@test.test"})
        view = PasswordResetEmailView.as_view()
        res = view(req)
        data = res.data
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            str(data["message"]),
            "メールアドレスにパスワードリセット用の確認コードを送信しました。コードを入力してパスワードの再設定を完了させてください。")
        self.assertEqual(AuthDigit.objects.filter(user=self.user).count(), 1)
        self.assertEqual(len(mail.outbox), 1)

    def test_post_user_error(self):
        factory = RequestFactory()
        req = factory.post("/api/password/email/", {"email": "user@test.test"})
        view = PasswordResetEmailView.as_view()
        res = view(req)
        data = res.data
        self.assertEqual(res.status_code, 400)
        self.assertEqual(str(data["message"]), "登録されたユーザーが見つかりませんでした。")
        self.assertEqual(AuthDigit.objects.filter(user=self.user).count(), 0)
        self.assertEqual(len(mail.outbox), 0)

    def test_post__too_many_email_request_error(self):
        AuthDigit.objects.create(user=self.user)
        factory = RequestFactory()
        req = factory.post("/api/password/email/", {"email": "test@test.test"})
        view = PasswordResetEmailView.as_view()
        res = view(req)
        data = res.data
        self.assertEqual(res.status_code, 400)
        self.assertEqual(str(data["message"]),
                         "メールは短時間に連続して送ることができません。お手数ですが時間を空けてからお試しください。")
        self.assertEqual(AuthDigit.objects.filter(user=self.user).count(), 1)
        self.assertEqual(len(mail.outbox), 0)

    @mock.patch("main.models.AuthDigit.send_password_reset_email")
    def test_post_email_error(self, mock):
        mock.side_effect = Exception()
        factory = RequestFactory()
        req = factory.post("/api/password/email/", {"email": "test@test.test"})
        view = PasswordResetEmailView.as_view()
        res = view(req)
        data = res.data
        self.assertEqual(res.status_code, 500)
        self.assertEqual(
            str(data["message"]),
            "メールの送信に失敗しました。少しお待ちいただいてからもう一度送っていただくか、サービス運営者にお問合せください。")
        self.assertEqual(AuthDigit.objects.filter(user=self.user).count(), 0)
        self.assertEqual(len(mail.outbox), 0)
