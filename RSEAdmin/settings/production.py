"""
Django settings for RSEAdmin project PRODUCTION.

"""
import json
import os
from django.core.exceptions import ImproperlyConfigured

from .base import *

# ----------------------------------------------------------------------------
# Debug Settings
# ----------------------------------------------------------------------------
# SECURITY WARNING: never run with debug turned on in PRODUCTION!
# (WHICH IS WHAT THIS FILE IS FOR)
# ----------------------------------------------------------------------------

DEBUG = TEMPLATE_DEBUG = False

# ----------------------------------------------------------------------------
# Import local production settings from secrets.json file
# Provide get function
# ----------------------------------------------------------------------------
# SECURITY WARNING: never upload secrets.json to any public repository!
# ----------------------------------------------------------------------------

with open(os.path.join(BASE_DIR, 'secrets.json')) as secrets_file:
    secrets = json.load(secrets_file)

def get_secret(setting, secrets=secrets):
    """Get secret setting or fail with ImproperlyConfigured"""
    try:
        return secrets[setting]
    except KeyError:
        raise ImproperlyConfigured("Set the {} setting".format(setting))


# ----------------------------------------------------------------------------
# Security Settings
# ----------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/2.2/topics/security/#ssl-https
# ----------------------------------------------------------------------------
# SECURE_HSTS_SECONDS:
# - 3600 = 1 hour
# - 31536000 = 1 year
# ----------------------------------------------------------------------------

SECRET_KEY = get_secret('SECRET_KEY')

# UNCOMMENT THESE WHEN SSL IS WORKING
# -----------------------------------
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

SECURE_SSL_REDIRECT = True

# UNCOMMENT/SET THIS WHEN YOU'RE SUPER CONVINCED THAT SSL IS WORKING
# ------------------------------------------------------------------
# SECURE_HSTS_SECONDS = 31536000

# ----------------------------------------------------------------------------
# Database Settings
# ----------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/2.2/ref/settings/#databases
# ----------------------------------------------------------------------------

DB_NAME = get_secret('DB_NAME')
DB_USER = get_secret('DB_USER')
DB_PASSWORD = get_secret('DB_PASSWORD')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': 'localhost',
        'PORT': '',
    }
}

# ----------------------------------------------------------------------------
# Host Settings
# ----------------------------------------------------------------------------
# Hosts/domain names that are valid for this site
# REQUIRED if DEBUG is False
# See: https://docs.djangoproject.com/en/2.2/ref/settings/#allowed-hosts
# ----------------------------------------------------------------------------

SITE_FQDN = get_secret('SITE_FQDN')

ALLOWED_HOSTS = [
    SITE_FQDN,
    'localhost',
    '127.0.0.1',
]

INTERNAL_IPS = [
    '127.0.0.1',
]

# ----------------------------------------------------------------------------
# Disable the standard Django Admin site
# ----------------------------------------------------------------------------

ADMIN_ENABLED = False

# ----------------------------------------------------------------------------
# Default static root settings
# ----------------------------------------------------------------------------

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
