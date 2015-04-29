###---< AUTH >---###
import os
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Secret Key is env variable
SECRET_KEY = os.environ['SECRET_KEY']

from os.path import (dirname, basename)

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLOWED_HOSTS = ['*']

###---< Database >---###
import dj_database_url

DATABASES = {
    'default': dj_database_url.config()
}
# Absolute filesystem path to the top-level project folder:
SITE_ROOT = dirname(PROJECT_DIR)

# Site name:
SITE_NAME = basename(PROJECT_DIR)


# # Email Config if we have it
# EMAIL_PORT = os.environ['EMAIL_PORT']
# EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
# EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']

###---< Static Files >---####
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'


# Support for X-Request-ID
# NOTE: Code From Heroku Website

LOG_REQUEST_ID_HEADER = 'HTTP_X_REQUEST_ID'
LOG_REQUESTS = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'request_id': {
            '()': 'log_request_id.filters.RequestIDFilter'
        }
    },
    'formatters': {
        'standard': {
            'format': '%(levelname)-8s [%(asctime)s] [%(request_id)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'filters': ['request_id'],
            'formatter': 'standard',
        },
    },
    'loggers': {
        'log_request_id.middleware': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}

