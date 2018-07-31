from .base import *

SECRET_KEY = '76)5(c(fx4ton1h6ski0r1t3y9f$!q#q68+-drj3m&tmb9o8u_'
DEBUG = True
ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
