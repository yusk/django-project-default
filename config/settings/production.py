import os
import pymysql

from .base import *

pymysql.install_as_MySQLdb()

DEBUG = False
SECRET_KEY = os.environ.get('DB_SECRET_KEY')
JWT_AUTH['JWT_SECRET_KEY'] = SECRET_KEY
ALLOWED_HOSTS = [os.environ.get('PRODUCTION_HOST')]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}
