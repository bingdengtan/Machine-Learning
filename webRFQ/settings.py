"""
Django settings for webRFQ project.

Generated by 'django-admin startproject' using Django 2.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import datetime
import sys
import mongoengine
from keras.models import load_model

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+ln#be45z5ah%@*+4s&s8@68x(yhr^ef^6pl3ts%o&fgvdnt@q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_mongoengine',
    'rest_framework_jwt',
    'corsheaders',
    'app'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'webRFQ.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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


WSGI_APPLICATION = 'webRFQ.wsgi.application'

# Allow all hosts.
CORS_ORIGIN_ALLOW_ALL = True

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'sql_server.pyodbc',
        'NAME': 'WebRFQ',
        'HOST': '172.19.33.124',
        'PORT': '1433',
        'USER': 'bireadonly',
        'PASSWORD': 'JEM@t0r!',
        'OPTIONS': {
            'driver':'SQL Server Native Client 11.0',
            'MARS_Connection': True,
        }
    }
}

# We define 2 Mongo databases - default and test
MONGODB_DATABASES = {
    "default": {
        "name": "ML",
        "host": "172.19.33.239",
        "port": 27017,
        "tz_aware": True,  # if you use timezones in django (USE_TZ = True)
    },

    "test": {
        "name": "ML",
        "host": "172.19.33.239",
        "port": 27017,
        "tz_aware": True,  # if you use timezones in django (USE_TZ = True)
    }
}

def is_test():
    """
    Checks, if we're running the server for real or in unit-test.
    We might need a better implementation of this function.
    """
    if 'test' in sys.argv or 'testserver' in sys.argv:
        print("Using a test mongo database")
        return True
    else:
        print("Using a default mongo database")
        return False

if is_test():
    db = 'test'
else:
    db = 'default'

# establish connection with default or test database, depending on the management command, being run
# note that this connection syntax is correct for mongoengine0.9-, but mongoengine0.10+ introduced slight changes

mongoengine.register_connection(
    'ML',
    name=MONGODB_DATABASES[db]['name'],
    host=MONGODB_DATABASES[db]['host'],
    port=MONGODB_DATABASES[db]['port']
)

mongoengine.connect('ML', host='172.19.33.239', port=27017)

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(os.path.join(BASE_DIR, 'frontend/dist/client')),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Below is application settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'app.authentication.JSONWebTokenAuthentication',
        'app.authentication.IdentityTokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'app.core.pagination.StandardResultsSetPagination'
}

# Authentication via identity server
JWT_AUTH = {
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    'JWKS_URL': 'http://localhost:5555/.well-known/openid-configuration/jwks'
}

JWT_EXPIRATION_DELTA = datetime.timedelta(days=7)

ML_MODELS_ROOT = os.path.join(BASE_DIR, 'ml_models')
ML_MODEL = load_model(ML_MODELS_ROOT + '\\trained_model.h5')
import numpy as np
X = np.array([[1,1,1,1.,1.,1.,1.,1.,1]])
prediction = ML_MODEL.predict(X)
# prediction = prediction + 0.1159
# prediction = prediction / 0.0000036968
# print("Earnings Prediction for Proposed Product - ${}".format(prediction))