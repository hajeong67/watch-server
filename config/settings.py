"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.2.20.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-nc=9wm%ozwx@_c#yy!dr3b=^a)x+2g&sw5s*g^jwj+ls1@nba*"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['52.78.71.115']

# Application definition

SYSTEM_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    # 'rest_framework_gis',
    'rest_framework',
    'drf_spectacular',
    'django_celery_results',
    'channels',
]

CUSTOM_APPS = [
    'watch.apps.WatchConfig',
    'users.apps.UserConfig',
    'emotion.modules.apps.ModulesConfig',
    # 'logapp.apps.LogappConfig'
]

INSTALLED_APPS = SYSTEM_APPS + THIRD_PARTY_APPS + CUSTOM_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    'users.middleware.DeviceIDMiddleware',
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        'DIRS': [BASE_DIR / 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = 'config.asgi.application'

MEDIA_URL = '/uploads/'
MEDIA_ROOT = BASE_DIR / 'uploads'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': '52.78.71.115',
        'PORT': '5432',
        'NAME': 'watch_db',
        'USER': 'watch_user',
        'PASSWORD': 'watch_pass',
    }
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        # 'CONFIG': {
        #     'hosts': [
        #         (os.environ.get('REDIS_CHANNEL_LAYER_PRIMARY', LOCALHOST), 6379),
        #     ],
        # },
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },
    },
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Celery Configuration
CELERY_ENABLE_UTC = False
CELERY_TIMEZONE = 'Asia/Seoul'
# CELERY_BROKER_URL = f"redis://{os.environ.get('REDIS_SESSION_STORAGE_PRIMARY', LOCALHOST)}:6379/0"
# CELERY_BROKER_URL = 'redis://172.17.0.3:6379/0'
# CELERY_BROKER_URL = 'redis://redis:6379/0'
# CELERY_BROKER_URL = f"redis://{os.environ.get('REDIS_SESSION_STORAGE_PRIMARY', '127.0.0.1')}:6379/0"
CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 7200}  # 1 hour
CELERY_RESULT_BACKEND = 'django-db'
# CELERY_REDBEAT_REDIS_URL = f"redis://{os.environ.get('REDIS_SESSION_STORAGE_PRIMARY', LOCALHOST)}:6379/1"

# Auth
AUTH_USER_MODEL = 'users.User'

# rest_framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

OPENSEARCH_URL = "search-watch-opensearch-domain-y2ayujgu47jvuwgv6vj4wl4et4.ap-northeast-2.es.amazonaws.com"

#spectular setting
SPECTACULAR_SETTINGS = {
    'TITLE': "Sensor Data API",
    'DESCRIPTION': "API documentation",
    'VERSION': "1.0.0",
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_SETTINGS': {
        'persistAuthorization': True,
    },
    'COMPONENT_SPLIT_REQUEST': True,
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': "JWT 인증을 위해 'Bearer <your_access_token>' 형식으로 입력하세요.",
        },
    },
    'SECURITY': [{'Bearer': []}],
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',  # console handler는 DEBUG 레벨
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',  # Django 관련 로거는 WARNING 레벨
            'propagate': True,
        },
        'logger': {
            'handlers': ['console'],
            'level': 'DEBUG',  # logger 로거는 DEBUG 레벨
            'propagate': False,
        },
    },
}

from watch.opensearch_client import client as opensearch_client