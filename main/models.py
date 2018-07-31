import uuid

from django.db import models
from django.contrib.auth.base_user import (
    AbstractBaseUser, BaseUserManager)
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import EmailValidator


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

    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
