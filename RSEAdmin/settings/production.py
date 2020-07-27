"""
Django settings for RSEAdmin project PRODUCTION.

"""
import json
import ldap
import logging
import os

from django_auth_ldap.config import LDAPSearch
from django.core.exceptions import ImproperlyConfigured

from RSEAdmin.auth import GroupMembershipDNGroupType

from .base import *

logger = logging.getLogger('django_auth_ldap')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

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
# Authentication Backend and LDAP Settings
# ----------------------------------------------------------------------------
# 
# ----------------------------------------------------------------------------

AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_LDAP_GLOBAL_OPTIONS = {
    ldap.OPT_X_TLS_REQUIRE_CERT: False,
    ldap.OPT_REFERRALS: False,
}

AUTH_LDAP_SERVER_URI = get_secret('AUTH_LDAP_SERVER_URI')
AUTH_LDAP_BIND_DN = ''
AUTH_LDAP_BIND_PASSWORD = ''
AUTH_LDAP_ALWAYS_UPDATE_USER = True
AUTH_LDAP_GROUP_TYPE = GroupMembershipDNGroupType()
AUTH_LDAP_USER_SEARCH = LDAPSearch(get_secret('AUTH_LDAP_USER_SEARCH_ARGS'), ldap.SCOPE_SUBTREE, "(uid=%(user)s)")
AUTH_LDAP_GROUP_SEARCH = LDAPSearch(get_secret('AUTH_LDAP_GROUP_SEARCH_ARGS'), ldap.SCOPE_SUBTREE, "(uid=%(user)s)")
AUTH_LDAP_REQUIRE_GROUP = get_secret('AUTH_LDAP_REQUIRE_GROUP')
AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail",
}
AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    "is_staff": get_secret('XAUTH_LDAP_SUPERUSER_GROUP'),
    "is_superuser": get_secret('XAUTH_LDAP_SUPERUSER_GROUP'),
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
