import os
import uuid

from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.base_user import (
    AbstractBaseUser, BaseUserManager)
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import EmailValidator
from django.core.mail import send_mail

from main.decorators import delete_previous_file


def icon_file_path(instance, filename):
    return "icon/%s%s" % (timezone.now(), os.path.splitext(filename)[1])


class SoftDeletionQuerySet(models.QuerySet):
    def delete(self):
        return super().update(deleted_at=timezone.now())

    def hard_delete(self):
        return super().delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)


class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(deleted_at=None)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class SoftDeletionModel(models.Model):
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super().delete()


class UserManager(BaseUserManager):
    use_in_migrations = True

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


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=64, default='guest user')
    email = models.EmailField(max_length=254, unique=True, validators=[EmailValidator])
    password = models.CharField(max_length=254)

    icon = models.ImageField(upload_to=icon_file_path, null=True)

    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def send_mail(self, subject, content, from_email=settings.EMAIL_HOST_USER, fail_silently=False):
        send_mail(
            subject,
            content,
            from_email,
            [self.email],
            fail_silently=False,
        )

    @delete_previous_file
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    @delete_previous_file
    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)
