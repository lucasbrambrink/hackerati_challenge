"""

    HACKERATI AUCTION SETTINGS

"""

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

### Define DEBUG --> determine if production or not
import socket
hostname = socket.gethostname()
DEBUG = True if '192.168' in hostname else False

TEMPLATE_DEBUG = DEBUG

if DEBUG:  # not-production
    PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
else:  # production-settings
    PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ADMINS = (
    ('Lucas', 'lbrambrink@gmail.com'),
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'base',
    'auction',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'auction_hackerati.urls'

WSGI_APPLICATION = 'auction_hackerati.wsgi.application'

###---< Internationalization >---###

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

###---< Email Config >---###
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'


###---< Static files >---###
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_DIR, 'base', 'root')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'base', 'static', 'media')

STATICFILES_DIRS = (
    ('base', os.path.join(PROJECT_DIR, 'base', 'static', 'bower_components')),
    ('auction', os.path.join(PROJECT_DIR, 'auction', 'static')),
    ('images', os.path.join(PROJECT_DIR, 'base', 'static', 'media')),
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'base', 'static', 'templates'),
    os.path.join(PROJECT_DIR, 'auction', 'static', 'templates'),
)



###---< Import Local Settings >---###
if DEBUG:
    try:
        from auction_hackerati.local_settings import *
    except ImportError:
        raise 'Unable to import local settings file'

###---< Production Settings >---###
else:
    try:
        from auction_hackerati.production_settings import *
    except ImportError:
        raise 'Unable to load production settings'
