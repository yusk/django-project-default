from unittest import mock
from datetime import datetime

from django.test import TestCase
from django.core import mail
from django.utils import timezone

from main.models import User


class UserModelTest(TestCase):
    def setUp(self):
        tz = timezone.get_current_timezone()
        dt = datetime(2021, 3, 4, 14, 57, 11, 703055)
        self.mock_date = tz.localize(dt)
        with mock.patch("django.utils.timezone.now") as mock_now:
            mock_now.return_value = self.mock_date
            self.user = User.objects.create_user(email="test@test.test",
                                                 password="12345",
                                                 name="test_user")

    def test_default_value(self):
        self.assertEqual(self.user.name, "test_user")
        self.assertEqual(self.user.email, "test@test.test")
        self.assertTrue(self.user.check_password("12345"))
        self.assertFalse(self.user.icon)
        self.assertFalse(self.user.email_confirmed)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        self.assertEqual(self.user.created_at, self.mock_date)
        self.assertIsNone(self.user.deleted_at)

    def test_delete(self):
        self.user.delete()
        self.assertEqual(self.user.email,
                         f"test@test.test.{self.user.id}.deleted")
        self.assertIsNotNone(self.user.deleted_at)

    def test_delete_deleted__at_is_not_none(self):
        self.user.deleted_at = self.mock_date
        self.user.save()
        self.assertFalse(self.user.delete())

    def test_revive(self):
        self.user.email = f"test@test.test.{self.user.id}.deleted"
        self.user.save()
        self.user.revive()
        self.assertEqual(self.user.email, "test@test.test")
        self.assertIsNone(self.user.deleted_at)

    def test_revive_not_deleted(self):
        self.assertFalse(self.user.revive())

    def test_send_email(self):
        self.user.send_email('subject', "content")
        self.assertEqual(len(mail.outbox), 1)
