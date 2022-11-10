from unittest import mock
from datetime import datetime

from django.test import TestCase
from django.test.client import RequestFactory
from django.core import mail
from django.utils import timezone

from main.models import User
from main.models.auth import AuthDigit
from main.views import RegisterDummyUserView, RegisterUUIDView, RegisterUserViewWithEmail


class RegisterDummyUserViewTest(TestCase):
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
        req = factory.post("/api/register/dummy/")
        view = RegisterDummyUserView.as_view()
        res = view(req)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(User.objects.filter(name="dummy user").count(), 1)


class RegisterUUIDViewTest(TestCase):
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
        req = factory.post("/api/register/uuid/",
                           {"uuid": "3fa85f64-5717-4562-b3fc-2c963f66afa6"},
                           content_type="application/json")
        view = RegisterUUIDView.as_view()
        res = view(req)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            User.objects.filter(
                device_uuid="3fa85f64-5717-4562-b3fc-2c963f66afa6").count(), 1)

    def test_post_already_exists_error(self):
        factory = RequestFactory()
        req = factory.post("/api/register/uuid/",
                           {"uuid": "7278cacb-f173-4ef9-b00f-bdbe68647c8d"},
                           content_type="application/json")
        view = RegisterUUIDView.as_view()
        res = view(req)
        data = res.data
        self.assertEqual(res.status_code, 400)
        self.assertEqual(str(data["detail"]), "すでにそのユーザーは登録済みです。")


class RegisterUserViewWithEmailTest(TestCase):
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
        req = factory.post("/api/register/user/", {
            "id": "test",
            "email": "user@test.test",
            "password": "testpass",
            "password_confirm": "testpass"
        },
                           content_type="application/json")
        view = RegisterUserViewWithEmail.as_view()
        res = view(req)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            User.objects.filter(email="user@test.test").count(), 1)
        self.assertEqual(len(mail.outbox), 1)

    def test_post_password_characters_error(self):
        factory = RequestFactory()
        req = factory.post("/api/register/user/", {
            "id": "test",
            "email": "user@test.test",
            "password": "test",
            "password_confirm": "test"
        },
                           content_type="application/json")
        view = RegisterUserViewWithEmail.as_view()
        res = view(req)
        self.assertEqual(res.status_code, 400)
        data = res.data
        self.assertIn("password", data)
        self.assertEqual(str(data["password"][0]), "この項目は少なくとも8文字以上にしてください。")
        self.assertIn("password_confirm", data)
        self.assertEqual(str(data["password_confirm"][0]),
                         "この項目は少なくとも8文字以上にしてください。")

    def test_post_password_confirm_error(self):
        factory = RequestFactory()
        req = factory.post("/api/register/user/", {
            "id": "test",
            "email": "user@test.test",
            "password": "testpass",
            "password_confirm": "testuser"
        },
                           content_type="application/json")
        view = RegisterUserViewWithEmail.as_view()
        res = view(req)
        self.assertEqual(res.status_code, 400)
        data = res.data
        self.assertIn("password_confirm", data)
        self.assertEqual(str(data["password_confirm"][0]),
                         "パスワード確認がパスワードと一致していません。")

    def test_post_email_error(self):
        factory = RequestFactory()
        req = factory.post("/api/register/user/", {
            "id": "test",
            "email": "test@test.test",
            "password": "testpass",
            "password_confirm": "testpass"
        },
                           content_type="application/json")
        view = RegisterUserViewWithEmail.as_view()
        res = view(req)
        self.assertEqual(res.status_code, 400)
        data = res.data
        self.assertIn("email", data)
        self.assertEqual(str(data["email"][0]), "このメールアドレスは既に登録されています。")

    def test_post__too_many_email_request_error(self):
        AuthDigit.objects.create(
            user=User(id="test", email="user@test.test", password="testpass"))
        factory = RequestFactory()
        req = factory.post("/api/register/user/", {
            "id": "test",
            "email": "user@test.test",
            "password": "testpass",
            "password_confirm": "testpass"
        },
                           content_type="application/json")
        view = RegisterUserViewWithEmail.as_view()
        res = view(req)
        data = res.data
        self.assertEqual(res.status_code, 400)
        self.assertEqual(str(data["message"]),
                         "メールは短時間に連続して送ることができません。お手数ですが時間を空けてからお試しください。")
        self.assertEqual(
            User.objects.filter(email="user@test.test").count(), 0)

    @mock.patch("main.models.auth.AuthDigit.send_confirm_email")
    def test_post__send_email_error(self, mock):
        mock.side_effect = Exception("テスト")
        factory = RequestFactory()
        req = factory.post("/api/register/user/", {
            "id": "test",
            "email": "user@test.test",
            "password": "testpass",
            "password_confirm": "testpass"
        },
                           content_type="application/json")
        view = RegisterUserViewWithEmail.as_view()
        res = view(req)
        data = res.data
        self.assertEqual(res.status_code, 500)
        self.assertEqual(
            str(data["message"]),
            "メールの送信に失敗しました。少しお待ちいただいてからもう一度送っていただくか、サービス運営者にお問合せください。")
        self.assertEqual(
            User.objects.filter(email="user@test.test").count(), 0)
