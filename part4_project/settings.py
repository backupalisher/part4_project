import os
import sys

from .env import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_ROOT = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '59bh9hwmjovry$@gjah!7pe5vrh*d+&_srj=udw*^w0w*y81ds'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = DEBUG_STATE

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    '.d.part4.info',
    'www.d.part4.info',
    'part4.info',
    'www.part4.info',
    'part4.ru',
    'www.part4.ru'
]

INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    # 'silk',
    'debug_toolbar',
    'compressor',
    'el_pagination',
    'db_model',
    'search',
    'main',
    'user_passport',
    'detail',
    'model',
    'about',
    'contacts',
    'brand',
    'filter',
    'cartridge'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'silk.middleware.SilkyMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'part4_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                "context_processors.views.main_menu",
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'part4_project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DEFAULT_NAME,
        'USER': DEFAULT_USER,
        'PASSWORD': DEFAULT_PASS,
        'HOST': HOST,
        'PORT': DEFAULT_PORT
    },
    'part4': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': PART4_NAME,
        'USER': PART4_USER,
        'PASSWORD': PART4_PASS,
        'HOST': HOST,
        'PORT': DEFAULT_PORT
    }
}

DATABASE_ROUTERS = ['db_model.router.part4router']

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

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
        os.path.join(PROJECT_ROOT, "static"),
    )

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'image')
MEDIA_URL = 'https://storage.yandexcloud.net/part4images/images/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

EL_PAGINATION_PER_PAGE = 16
