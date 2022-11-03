import os

PRODUCTION_HOST = os.environ.get('PRODUCTION_HOST')

DB_SECRET_KEY = os.environ.get('DB_SECRET_KEY')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', 3306)

CORS_ORIGIN_WHITELIST = os.environ.get(
    'CORS_ORIGIN_WHITELIST',
    'http://localhost:3000,http://127.0.0.1:3000').split(',')

SLACK_WEBHOOK_URL = os.environ.get('SLACK_WEBHOOK_URL')

IGNORE_GOOGLE_ANALYTICS = bool(os.environ.get('IGNORE_GOOGLE_ANALYTICS'))

STRIPE_API_KEY = os.environ.get('STRIPE_API_KEY')
STRIPE_API_SECRET = os.environ.get('STRIPE_API_SECRET')

TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = bool(os.environ.get('EMAIL_USE_TLS'))

CONFIRM_EMAIL = os.environ.get('CONFIRM_EMAIL')
SERVICE_NAME = os.environ.get('SERVICE_NAME')
SERVICE_COPY = os.environ.get('SERVICE_COPY')
COMPANY_NAME = os.environ.get('COMPANY_NAME')
