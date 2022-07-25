"""
Django settings for cf project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from pathlib import Path
from django.contrib import admin

import cf.db as db

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'be-a!7vw2o_n4@z+0kv0es2j50n3$81kf@*^4k+r=tauwfca#7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', 'ifmlinares.pythonanywhere.com', '*']

# Application definition
INSTALLED_APPS = [
    'jet.dashboard',
    'jet',
    'django.contrib.admin',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # another libraries with django
    'django.contrib.sites',

    # django all auth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # 'allauth.socialaccount.providers.facebook'
    # 'allauth.socialaccount.providers.google',
    'django.contrib.humanize',
    'paypal.standard.ipn',
    'embed_video',
    'ckeditor',
    # own apps
    'apps.core',
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

ROOT_URLCONF = 'cf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'cf.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = db.SQLITE


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'es-ve'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# django allauth AUTHENTICATION_BACKENDS
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

AUTH_USER_MODEL = 'core.User'

SITE_ID = 1

ACCOUNT_SIGNUP_FORM_CLASS = 'apps.core.forms.SignupForm.SignupForm'
# USER LOGIN
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# REQUIREMENTS WITH LOGIN
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "none"
EMAIL_TIMEOUT = 5
EMAIL_USE_TLS = True
# SEND AUTHENTICATION EMAIL HOST
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = DEFAULT_FROM_EMAIL = 'titolfalcon1@gmail.com'
EMAIL_HOST_PASSWORD = '12022021Ab$'
EMAIL_SUBJECT_PREFIX = 'Miguel Linares'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

LOGIN_REDIRECT_URL = '/'

#  PAYPAL SETTINGS
PAYPAL_TEST = False
PAYPAL_RECEIVER_EMAIL = 'Luis.huerta.2507@gmail.com'

# Django Jet settings
# admin.site.site_header = "Administración Cositas Favoritas"

JET_SIDE_MENU_ITEMS = [
    # {'label': 'Usuarios','app_label': 'auth', 'items': [
    #     {'name': 'group'},
    # ]},
    {'app_label': 'core', 'items': [
        {'name': 'order'},
        {'name': 'item'},
        # {'name': 'address'},
        # {'name': 'billingaddress'},
        {'name': 'user'},
    ]},
    # {'app_label': 'core', 'items': [

    #     {'name': 'coloritem'},
    #     {'name': 'cantitem'},
    # ]},
    # {'app_label': 'account', 'items': [
    #     {'name': 'emailaddress'},
    # ]},
    # {'app_label': 'ipn', 'items': [
    #     {'name': 'paypalipn'},
    # ]},
    {'app_label': 'sites', 'items': [
        {'name': 'site'},
    ]},
]

JET_SIDE_MENU_COMPACT = True
JET_CHANGE_FORM_SIBLING_LINKS = True

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
    },
}