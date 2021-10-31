import datetime
import random
import secrets

from django.db import models
from django.utils import timezone

from main.constants import (DIGIT_AUTH_EXPIRED_MINUTES, CONFIRM_EMAIL_SUBJECT,
                            CONFIRM_EMAIL_CONTENT,
                            PASSWORD_RESET_EMAIL_SUBJECT,
                            PASSWORD_RESET_EMAIL_CONTENT)
from main.env import CONFIRM_EMAIL, SERVICE_NAME, SERVICE_COPY, COMPANY_NAME


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

    def is_expired(self):
        return timezone.now() > self.expired_at

    def reset(self):
        self.code = random_digit_code()
        self.expired_at = gen_expired_at()
        self.save()

    def send_confirm_email(self):
        subject = CONFIRM_EMAIL_SUBJECT.format(name=SERVICE_NAME)
        content = CONFIRM_EMAIL_CONTENT.format(company=COMPANY_NAME,
                                               copy=SERVICE_COPY,
                                               name=SERVICE_NAME,
                                               code=self.code,
                                               email=CONFIRM_EMAIL)
        self.user.send_email(subject=subject,
                             content=content,
                             from_email=CONFIRM_EMAIL)

    def send_password_reset_email(self):
        subject = PASSWORD_RESET_EMAIL_SUBJECT.format(name=SERVICE_NAME)
        content = PASSWORD_RESET_EMAIL_CONTENT.format(company=COMPANY_NAME,
                                                      copy=SERVICE_COPY,
                                                      name=SERVICE_NAME,
                                                      code=self.code,
                                                      email=CONFIRM_EMAIL)
        self.user.send_email(subject=subject,
                             content=content,
                             from_email=CONFIRM_EMAIL)

    @classmethod
    def update_or_create(cls, user):
        auth = cls.objects.filter(user=user).first()
        if auth:
            auth.code = random_digit_code()
            auth.expired_at = gen_expired_at()
            auth.save()
        else:
            auth = cls.objects.create(user=user)
        return auth


class PasswordResetToken(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    token = models.CharField(max_length=32, default=secrets.token_urlsafe)
    expired_at = models.DateTimeField(default=gen_expired_at)

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
