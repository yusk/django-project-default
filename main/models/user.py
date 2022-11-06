import os
import uuid
import base64
import io

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.base_user import (AbstractBaseUser, BaseUserManager)
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from rest_framework_jwt.settings import api_settings

from main.env import EMAIL_HOST_USER

from ._base import SoftDeletionModel, SoftDeletionManager, SoftDeletionQuerySet

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


def icon_file_path(instance, filename):
    return "icon/%s%s" % (timezone.now(), os.path.splitext(filename)[1])


class UserQuerySet(SoftDeletionQuerySet):
    def delete(self):
        cnt = 0
        for user in self:
            cnt += user.delete()
        return cnt

    def revive(self):
        cnt = 0
        for user in self:
            cnt += user.revive()
        return cnt


class UserManager(SoftDeletionManager, BaseUserManager):
    use_in_migrations = True
    queryset_class = UserQuerySet

    def _create_user(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        if password is None:
            user = self.model(email=email, **extra_fields)
            user.set_unusable_password()
        else:
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_guest_user(self, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        if 'email' in extra_fields:
            email = extra_fields['email']
            del extra_fields['email']
        else:
            email = "%s@guest.com" % str(uuid.uuid4())
        return self._create_user(email, **extra_fields)

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


class User(SoftDeletionModel, PermissionsMixin, AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=64, default='', blank=True)
    email = models.EmailField(max_length=254,
                              unique=True,
                              validators=[EmailValidator],
                              db_index=True)
    password = models.CharField(max_length=254)

    icon = models.ImageField(upload_to=icon_file_path, null=True, blank=True)
    device_uuid = models.UUIDField(default=uuid.uuid4)
    email_confirmed = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    objects = UserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def delete(self):
        if self.deleted_at:
            return 0
        self.email = f"{self.email}.{self.id}.deleted"
        self.deleted_at = timezone.now()
        self.save()
        return 1

    def revive(self):
        suffix = f".{self.id}.deleted"
        if not self.email.endswith(suffix):
            return 0
        self.email = self.email[:-len(suffix)]
        self.deleted_at = None
        self.save()
        return 1

    def save(self, *args, **kwargs):
        # self.full_clean()
        return super().save(*args, **kwargs)

    def clean(self, *args, **kwargs):
        if self.is_superuser and not self.is_staff:
            raise ValidationError({"is_staff": "スーパーユーザーはスタッフでなければなりません。"})
        super().clean(*args, **kwargs)

    def send_email(self,
                   subject,
                   content,
                   from_email=EMAIL_HOST_USER,
                   fail_silently=False):
        send_mail(
            subject,
            content,
            from_email,
            [self.email],
            fail_silently=fail_silently,
        )

    def save_icon_with_base64(self, base64_str):
        img = io.BytesIO(base64.b64decode(base64_str.encode()))
        self.icon.save("icon.png", img)

    def get_jwt(self):
        payload = jwt_payload_handler(self)
        return jwt_encode_handler(payload)
