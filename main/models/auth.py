import datetime
import random
import secrets

from django.db import models
from django.utils import timezone
from django.db.models.manager import BaseManager

from main.constants import (DIGIT_AUTH_EXPIRED_MINUTES, EMAIL_LIMIT_MINUTES,
                            EMAIL_LIMIT_MESSAGE, LOGIN_INVALID_MINUTES,
                            LOGIN_INVALID_COUNT, LOGIN_INVALID_MESSAGE,
                            ConstantProvider)
from main.env import CONFIRM_EMAIL
from main.errors import TooManyEmailRequestError

from ._base import WithExpiredQuerySet


def random_digit_code():
    num = random.randint(1, 999999)
    return f"{num:06d}"


def gen_expired_at():
    return datetime.datetime.now() + datetime.timedelta(
        minutes=DIGIT_AUTH_EXPIRED_MINUTES)


class AuthDigit(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    code = models.CharField(max_length=6, default=random_digit_code)
    expired_at = models.DateTimeField(default=gen_expired_at)

    objects = BaseManager.from_queryset(WithExpiredQuerySet)()

    def is_expired(self):
        return timezone.now() > self.expired_at

    def reset(self):
        self.code = random_digit_code()
        self.expired_at = gen_expired_at()
        self.save()

    def send_confirm_email(self):
        subject = ConstantProvider.confirm_email_subject()
        content = ConstantProvider.confirm_email_content(self.code)
        self.user.send_email(subject=subject,
                             content=content,
                             from_email=CONFIRM_EMAIL)

    def send_password_reset_email(self):
        subject = ConstantProvider.password_reset_email_subject()
        content = ConstantProvider.password_reset_email_content(self.code)
        self.user.send_email(subject=subject,
                             content=content,
                             from_email=CONFIRM_EMAIL)

    @classmethod
    def update_or_create(cls, user):
        auth = cls.objects.filter(user=user).first()
        if auth is None:
            auth = cls.objects.create(user=user)
        elif timezone.now() <= auth.updated_at + datetime.timedelta(
                minutes=EMAIL_LIMIT_MINUTES):
            message = "メールは短時間に連続して送ることができません。お手数ですが時間を空けてからお試しください。"
            raise TooManyEmailRequestError(message=message)
        else:
            auth.code = random_digit_code()
            auth.expired_at = gen_expired_at()
            auth.save()

        return auth


class PasswordResetToken(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    token = models.CharField(max_length=32, default=secrets.token_urlsafe)
    expired_at = models.DateTimeField(default=gen_expired_at)

    objects = BaseManager.from_queryset(WithExpiredQuerySet)()

    def is_expired(self):
        return timezone.now() > self.expired_at

    @classmethod
    def update_or_create(cls, user):
        token = cls.objects.filter(user=user).first()
        if token:
            token.token = secrets.token_urlsafe()
            token.expired_at = gen_expired_at()
            token.save()
        else:
            token = cls.objects.create(user=user)
        return token


class LoginInvalid(models.Model):
    address = models.CharField(max_length=15)
    count = models.IntegerField(default=1)

    denied_at = models.DateTimeField(default=timezone.now)

    @classmethod
    def invalid(cls, address):
        obj = cls.objects.filter(
            address=address,
            denied_at__gt=timezone.now() -
            datetime.timedelta(minutes=LOGIN_INVALID_MINUTES)).first()

        if obj and obj.count == LOGIN_INVALID_COUNT:
            return LOGIN_INVALID_MESSAGE

        return None

    @classmethod
    def inc(cls, address):
        obj = cls.objects.filter(
            address=address,
            denied_at__gt=timezone.now() -
            datetime.timedelta(minutes=LOGIN_INVALID_MINUTES)).first()

        if obj:
            obj.count += 1
            obj.save()
            return

        obj = cls.objects.filter(address=address).exclude(
            count=LOGIN_INVALID_COUNT).first()

        if obj:
            obj.count = 1
            obj.denied_at = timezone.now()
            obj.save()
        else:
            cls.objects.create(address=address)
