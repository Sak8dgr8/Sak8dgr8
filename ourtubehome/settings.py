"""
Django settings for ourtubehome project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/

"""
import io
import os
from urllib.parse import urlparse
import django_heroku
import dj_database_url
from decouple import config

import environ
from google.cloud import secretmanager
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-uc74ebsba3dgpo79*d_1531_3e6)u-4j1=zjqbk16nauan3(02'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True




ALLOWED_HOSTS = ['localhost',
                  'www.our-tube.com',
                  'our-tube.com','*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'members',
    'widget_tweaks',
    'localflavor',
    'paypal.standard.ipn',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'ourtubehome.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, "ourtubehome/templates"],
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

WSGI_APPLICATION = 'ourtubehome.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

STATICFILES_DIRS = [BASE_DIR / 'ourtubehome/static', BASE_DIR / 'members/static']

STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'members/static/media')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
 
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'bvssaket6000@gmail.com'  # Replace with your Gmail address
EMAIL_HOST_PASSWORD = 'yfuawvzqudgjmnix'  # Replace with your Gmail password or app-specific password


SECURE_CROSS_ORIGIN_OPENER_POLICY='same-origin-allow-popups'

PAYPAL_RECEIVER_EMAIL = 'sb-lvreh26742576@business.example.com'
PAYPAL_TEST = True
PAYPAL_CLIENT_ID = 'AcFE-H9DzNPnUewQ484D6GmE1oXUpp0JUxK6DmchQPuWQFAyLN-Wr_Xf53H4wX13CFbZSB0GQ07_ZzMH'
PAYPAL_CLIENT_SECRET = 'ECmnv7vSVdr_isev2FsLhOWAoxiywAk-AtdWc2a6byhIaujdxwPNojgWiYJL_X9EH636gvxJFj5uz8-I'
PAYPAL_ENVIRONMENT = 'sandbox'

django_heroku.settings(locals())


