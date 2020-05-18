import os

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

DEBUG = True

ALLOWED_HOSTS = ['www.rodaschat.com','10.0.0.226', '127.0.0.1', 'localhost']

CORS_ORIGIN_WHITELIST = (
    'http://www.rodaschat.com',
    'https://www.rodaschat.com'
    'https://10.0.0.226'
)

CSRF_TRUSTED_ORIGINS = (
    'http://www.rodaschat.com',
    'https://www.rodaschat.com',
    'https://10.0.0.226'
)