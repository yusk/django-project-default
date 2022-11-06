from unittest import mock
from datetime import datetime
from uuid import UUID
import os

from django.test import TestCase
from django.conf import settings
from django.utils import timezone

from django.test.client import RequestFactory
from rest_framework.test import force_authenticate

from main.models import User
from main.views import UserView


class UserViewTest(TestCase):
    SAMPLE_BASE64_PATH = "sample/base64.txt"

    def setUp(self):
        tz = timezone.get_current_timezone()
        dt = datetime(2021, 3, 4, 14, 57, 11, 703055)
        self.mock_date = tz.localize(dt)
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = self.mock_date
            self.user = User.objects.create_user(name='test_user',
                                                 email='test@test.com',
                                                 password='password')

    def test_get_user(self):
        factory = RequestFactory()
        req = factory.get('/api/user/')
        force_authenticate(req, user=self.user)
        view = UserView.as_view()
        res = view(req)

        self.assertEqual(res.status_code, 200)
        data = res.data
        self.assertSetEqual(set(data.keys()), set(('id', 'name', 'icon')))
        self.assertIsInstance(UUID(data["id"]), UUID)
        self.assertEquals(data["name"], "test_user")
        self.assertIsNone(data["icon"])

    def test_put_user_name(self):
        factory = RequestFactory()
        req = factory.put('/api/user/', {'name': 'test_user2'},
                          content_type='application/json')
        force_authenticate(req, user=self.user)
        view = UserView.as_view()
        res = view(req)

        self.assertEqual(res.status_code, 200)
        data = res.data
        self.assertSetEqual(set(data.keys()), set(('id', 'name', 'icon')))
        self.assertIsInstance(UUID(data["id"]), UUID)
        self.assertEquals(data["name"], "test_user2")
        self.assertIsNone(data["icon"])

    def test_put_user_name_error(self):
        factory = RequestFactory()
        req = factory.put('/api/user/', {'name': 'a' * 65},
                          content_type='application/json')
        force_authenticate(req, user=self.user)
        view = UserView.as_view()
        res = view(req)

        self.assertEqual(res.status_code, 400)
        data = res.data
        self.assertIn("name", data)

    def test_put_user_icon(self):
        base64_path = os.path.join(settings.BASE_DIR, self.SAMPLE_BASE64_PATH)
        with open(base64_path, "r") as f:
            base64_str = f.read().replace('\\n', '\n')

        factory = RequestFactory()
        req = factory.put('/api/user/', {'icon_base64': base64_str},
                          content_type='application/json')
        force_authenticate(req, user=self.user)
        view = UserView.as_view()
        res = view(req)

        self.assertEqual(res.status_code, 200)
        data = res.data
        self.assertSetEqual(set(data.keys()), set(('id', 'name', 'icon')))
        self.assertIsInstance(UUID(data["id"]), UUID)
        self.assertEquals(data["name"], "test_user")
        self.assertIsNotNone(data["icon"])

    def test_delete_user(self):
        factory = RequestFactory()
        req = factory.delete("/api/user/", {"password": "password"},
                             content_type="application/json")
        force_authenticate(req, user=self.user)
        view = UserView.as_view()
        res = view(req)
        self.assertEqual(res.status_code, 204)
        self.assertFalse(User.objects.filter(id=self.user.id))
