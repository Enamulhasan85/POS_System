"""
Django settings for POS_System project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-v-c-eozrh&e*$a$=q(+)mav4(z-&!r+eckwy$8q+8d5xwff*1@'

# Read SECRET_KEY from an environment variable
import os
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'cg#p$g+j9tax!#a3cup@1$8obt2_+&k3q+pmu)5%asj6yjpkag')

## For example, for a site URL is at 'web-production-3640.up.railway.app'
## (replace the string below with your own site URL):
CSRF_TRUSTED_ORIGINS = ['https://web-production-45b2.up.railway.app']

# During development/for this tutorial you can instead set just the base URL
# CSRF_TRUSTED_ORIGINS = ['https://*.railway.app']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'

## For example, for a site URL at 'web-production-3640.up.railway.app'
## (replace the string below with your own site URL):https:///
ALLOWED_HOSTS = ['web-production-45b2.up.railway.app', '127.0.0.1']

# During development, you can instead set just the base URL
# (you might decide to change the site a few times).
# ALLOWED_HOSTS = ['.railway.com','127.0.0.1']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    "crispy_forms",
    "crispy_bootstrap5",
]

CRISPY_TEMPLATE_PACK = 'bootstrap5'
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'POS_System.urls'

SETTINGS_PATH = Path(__file__).resolve().parent.parent

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(SETTINGS_PATH, 'templates'),
                 os.path.join(SETTINGS_PATH, 'core', 'static', 'templates'),
                 os.path.join(SETTINGS_PATH, 'static', 'templates'),
                 BASE_DIR / 'static' / 'templates',
                ],
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

WSGI_APPLICATION = 'POS_System.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Update database configuration from $DATABASE_URL.
# import dj_database_url
# db_from_env = dj_database_url.config(conn_max_age=500)
# DATABASES['default'].update(db_from_env)


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



# The absolute path to the directory where collectstatic will collect static files for deployment.
STATIC_ROOT = BASE_DIR / 'static'

# The URL to use when referring to static files (where they will be served from)
STATIC_URL = '/static/'

# Simplified static file serving.
# https://pypi.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

import os

MEDIA_ROOT =  os.path.join(BASE_DIR, 'Uploads')
MEDIA_URL = '/Uploads/'
