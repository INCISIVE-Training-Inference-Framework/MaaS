import os
import logging.config
from pathlib import Path
import psycopg2.extensions

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Input variables
SECRET_KEY = os.getenv('SECRET_KEY', 'django_insecure')
DEBUG = os.getenv('DEBUG', 'True')
if DEBUG.lower() in ('yes', 'true', 't', 'y', '1'):
    DEBUG = True
else:
    DEBUG = False
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.2').split(',')

# Application definition

INSTALLED_APPS = [
    'main.apps.MainConfig',
    'rest_framework',
    'django_filters',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cleanup.apps.CleanupConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'maas.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'maas.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / '../storage/db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.{}'.format(os.getenv('DATABASE_ENGINE')),
            'NAME': os.getenv('DATABASE_NAME'),
            'USER': os.getenv('DATABASE_USERNAME'),
            'PASSWORD': os.getenv('DATABASE_PASSWORD'),
            'HOST': os.getenv('DATABASE_HOST'),
            'PORT': os.getenv('DATABASE_PORT'),
            'OPTIONS': {
                'isolation_level': psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE,
            }
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Madrid'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.getenv('STATIC_ROOT', '/static/')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Rest framework
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'maas.utils.StandardResultsSetPagination',
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'maas.utils.StandardResultsOrdering'
    ],
    'EXCEPTION_HANDLER': 'main.api.custom_exception_handler.custom_exception_handler'
}

# Files storage
MEDIA_ROOT = '../storage/files'
MEDIA_URL = '../storage/files/'

# Logging
if not DEBUG:
    # Clear prev config
    LOGGING_CONFIG = None

    # Get loglevel from env
    LOGLEVEL = os.getenv('LOGLEVEL', 'info').upper()

    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'console': {
                'format': '%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(module)s %(process)d %(thread)d %(message)s',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'console',
            },
        },
        'loggers': {
            '': {
                'level': LOGLEVEL,
                'handlers': ['console', ],
            },
        },
    })

# Domain

VALID_JOB_USE_CASES = {
    'training_from_scratch',
    'training_from_pretrained_model',
    'evaluating_from_pretrained_model',
    'merging_models',
    'inferencing_from_pretrained_model'
}

VALID_DATA_PARTNERS = os.getenv('VALID_DATA_PARTNERS', 'data-partner-1,data-partner-2').split(',')
VALID_DATA_PARTNERS = set(VALID_DATA_PARTNERS)
