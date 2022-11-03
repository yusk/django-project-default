from .base import *  # noqa

from main.env import (DB_SECRET_KEY, PRODUCTION_HOST, DB_NAME, DB_USER,
                      DB_PASSWORD, DB_HOST, DB_PORT)

DEBUG = False
SECRET_KEY = DB_SECRET_KEY
JWT_AUTH['JWT_SECRET_KEY'] = SECRET_KEY  # noqa
ALLOWED_HOSTS = [PRODUCTION_HOST]

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
