###---< AUTH >---###
import os
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Secret Key is env variable
SECRET_KEY = os.environ['SECRET_KEY']

from os.path import (dirname, basename)

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLOWED_HOSTS = ['*']


# Email Config
EMAIL_PORT = os.environ['EMAIL_PORT']
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']

###---< Database >---###
import dj_database_url

DATABASES = {
    'default': dj_database_url.config()
}

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'base', 'static'),
)
# Absolute filesystem path to the top-level project folder:
SITE_ROOT = dirname(PROJECT_DIR)
STATIC_ROOT = os.path.join(PROJECT_DIR, 'base', 'root')

# Site name:
SITE_NAME = basename(PROJECT_DIR)


# # Email Config if we have it
# EMAIL_PORT = os.environ['EMAIL_PORT']
# EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
# EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']

###---< Static Files >---####
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
