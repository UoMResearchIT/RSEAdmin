# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

import os
from .base import *

SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = False
ALLOWED_HOSTS = os.environ['DJANGO_ALLOWED_HOSTS'].split(',')
DEFAULT_FROM_EMAIL = os.environ['DJANGO_DEFAULT_FROM_EMAIL'].split(',')
SERVER_EMAIL = os.environ['DJANGO_SERVER_EMAIL'].split(',')

STATIC_ROOT = os.environ['DJANGO_STATIC_ROOT']
STATIC_URL = '/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DJANGO_DB_NAME'],
        'USER': os.environ['DJANGO_DB_USER'],
        'PASSWORD': os.environ['DJANGO_DB_PASSWORD'],
        'HOST': os.environ['DJANGO_DB_HOST'],
        'PORT': os.environ['DJANGO_DB_PORT'],
    }
}

# avoid transmitting the CSRF cookie over HTTP accidentally.
CSRF_COOKIE_SECURE = True
# Avoid transmitting the session cookie over HTTP accidentally.
SESSION_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True
X_FRAME_OPTIONS = 'DENY'
