import os

from .base import *  # noqa

from main.env import (DB_SECRET_KEY, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST,
                      DB_PORT)

DEBUG = False
SECRET_KEY = DB_SECRET_KEY
JWT_AUTH['JWT_SECRET_KEY'] = SECRET_KEY  # noqa
ALLOWED_HOSTS = os.environ.get('PRODUCTION_HOSTS', 'localhost').split(",")

# AWS
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

# AWS S3
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_STORAGE_REGION = os.environ.get("AWS_STORAGE_REGION")
AWS_S3_CUSTOM_DOMAIN = os.environ.get(
    "AWS_S3_CUSTOM_DOMAIN",
    f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_STORAGE_REGION}.amazonaws.com')
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'public/static'
AWS_DEFAULT_ACL = None
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
MEDIA_URL = '/public/media/'
STATICFILES_STORAGE = 'config.storage.StaticStorage'
DEFAULT_FILE_STORAGE = 'config.storage.MediaStorage'
AWS_CLOUDFRONT_KEY = os.environ.get('AWS_CLOUDFRONT_KEY', '').encode('ascii')
AWS_CLOUDFRONT_KEY_ID = os.environ.get('AWS_CLOUDFRONT_KEY_ID')

# AWS SES
EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_SES_REGION_NAME = os.environ.get("AWS_SES_REGION_NAME")
AWS_SES_REGION_ENDPOINT = f'email.{AWS_SES_REGION_NAME}.amazonaws.com'
DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_HOST_USER')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}
