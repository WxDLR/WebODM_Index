"""
Django settings for webodm project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os, sys, json

import datetime

import tzlocal
from django.contrib.messages import constants as messages

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

try:
    from .secret_key import SECRET_KEY
except ImportError:
    # This will be executed the first time Django runs
    # It generates a secret_key.py file that contains the SECRET_KEY
    from django.utils.crypto import get_random_string

    current_dir = os.path.abspath(os.path.dirname(__file__))
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    secret = get_random_string(50, chars)
    with open(os.path.join(current_dir, 'secret_key.py'), 'w') as f:
        f.write("SECRET_KEY='{}'".format(secret))
    SECRET_KEY=secret

    print("Generated secret key")

with open(os.path.join(BASE_DIR, 'package.json')) as package_file:
    data = json.load(package_file)
    VERSION = data['version']

TESTING = sys.argv[1:2] == ['test']
MIGRATING = sys.argv[1:2] == ['migrate']
WORKER_RUNNING = sys.argv[2:3] == ["worker"]

# SECURITY WARNING: don't run with debug turned on a public facing server!
DEBUG = os.environ.get('WO_DEBUG', 'YES') == 'YES' or TESTING
SESSION_COOKIE_SECURE = CSRF_COOKIE_SECURE = os.environ.get('WO_SSL', 'NO') == 'YES'
INTERNAL_IPS = ['127.0.0.1']

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django_filters',
    'app',
    'guardian',
    'rest_framework',
    'rest_framework_nested',
    'webpack_loader',
    'corsheaders',
    'colorfield',
    'imagekit',
    'codemirror2',
    'compressor',
    'nodeodm',
    'xadmin',
    'crispy_forms',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # use for MyUser Authentication
    'app.middleware.MyUserAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',


]

ROOT_URLCONF = 'webodm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'app', 'templates'),
            os.path.join(BASE_DIR, 'app', 'templates', 'app'),
            BASE_DIR
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'app.contexts.settings.load',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'webodm.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'webodm_dev',
        'USER': 'postgres',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
   {
       'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
   },
   {
       'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
   },
   {
       'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
   },
   {
       'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
   },
]

# Personal User Fields
AUTH_USER_MODEL = 'auth.User'

# Hook guardian
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend'
)

# Internationalization

LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = "Asia/Shanghai"
USE_I18N = True
USE_L10N = True
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'build', 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'app', 'static'),
]
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

# File Uploads
FILE_UPLOAD_MAX_MEMORY_SIZE = 4718592 # 4.5 MB
DATA_UPLOAD_MAX_NUMBER_FIELDS = None

FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'app.uploadhandler.TemporaryFileUploadHandler', # Ours doesn't keep file descriptors open by default
]

# Webpack
WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'app/bundles/',
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
    }
}


# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            # 'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARNING',
        },
        'app.logger': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'apscheduler.executors.default': {
            'handlers': ['console'],
            'level': 'WARNING',
        }
    }
}


# Auth
LOGIN_REDIRECT_URL = '/dashboard/'
LOGIN_URL = '/login/'

# CORS (very relaxed settings, users might want to change this in production)
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

# File uploads
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'app', 'media')
if TESTING:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'app', 'media_test')
MEDIA_TMP = os.path.join(MEDIA_ROOT, 'tmp')

# Store flash messages in cookies
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
MESSAGE_TAGS = {
    messages.ERROR: 'danger' # Bootstrap 3 compatibility
}

# REST setup
# Use Django's standard django.contrib.auth permissions (no anonymous usage)
REST_FRAMEWORK = {
  # 'DEFAULT_PERMISSION_CLASSES': [
  #   # 'app.permissions.GuardianObjectPermissions',
  # ],
  'DEFAULT_FILTER_BACKENDS': [
    # 'rest_framework.filters.DjangoObjectPermissionsFilter',
    'django_filters.rest_framework.DjangoFilterBackend',
    'rest_framework.filters.OrderingFilter',
  ],
  'DEFAULT_AUTHENTICATION_CLASSES': (
    # 'rest_framework.authentication.SessionAuthentication',
    # 'rest_framework.authentication.BasicAuthentication',
    'app.api.authentication.JSONWebTokenAuthentication',
  ),
  'PAGE_SIZE': 10,
  'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(hours=6),
}

# Compressor
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

# Sass
def theme(color):
    from app.contexts.settings import theme as f
    return f(color)


def complementary(color):
    from app.contexts.settings import complementary as f
    return f(color)


def scaleby(color, n):
    from app.contexts.settings import scaleby as f
    return f(color, n)


def scalebyiv(color, n):
    from app.contexts.settings import scaleby as f
    return f(color, n, True)


LIBSASS_CUSTOM_FUNCTIONS = {
    'theme': theme,
    'complementary': complementary,
    'scaleby': scaleby,
    'scalebyiv': scalebyiv
}

# Celery
CELERY_BROKER_URL = os.environ.get('WO_BROKER', 'redis://localhost')
CELERY_RESULT_BACKEND = os.environ.get('WO_BROKER', 'redis://localhost')

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_INCLUDE=['worker.tasks']
CELERY_WORKER_REDIRECT_STDOUTS = False
CELERY_WORKER_HIJACK_ROOT_LOGGER = False

if TESTING:
    CELERY_TASK_ALWAYS_EAGER = True

try:
    from .local_settings import *
except ImportError:
    pass
