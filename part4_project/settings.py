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
    '*',
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
    'rest_framework',
    'storages',
    # 'silk',
    # 'debug_toolbar',
    'compressor',
    'el_pagination',
    'sendmail',
    'accounts',
    'dashboard',
    'db_model',
    'search',
    'main_views',
    'main',
    'user_passport',
    'detail',
    'model',
    'about',
    'contacts',
    'brand',
    'filter',
    'supplies',
    'mathfilters',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'silk.middleware.SilkyMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'part4_project.urls'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

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
                "context_processors.views.currency",
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'part4_project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': DEFAULT_NAME,
    #     'USER': DEFAULT_USER,
    #     'PASSWORD': DEFAULT_PASS,
    #     'HOST': HOST,
    #     'PORT': DEFAULT_PORT
    # },
    'default': {
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

LANGUAGES = (
    ('ru', 'Russian'),
    ('en', 'English'),
)

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_REDIRECT_URL = '/account/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

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

DEFAULT_FILE_STORAGE = 'https://storage.yandexcloud.net/part4images/images/'
AWS_ACCESS_KEY_ID = 'qYopnnQ3T-9pP42mPVBz'
AWS_SECRET_ACCESS_KEY = 'Indwm3AaawrvDBUYwqKl8gPbQ2GKrcN2SWGslTds'
AWS_STORAGE_BUCKET_NAME = 'part4images'
AWS_S3_REGION_NAME = 'ru-central1'

if DEBUG:
    SITE_ID = 2
else:
    SITE_ID = 1

X_FRAME_OPTIONS = 'ALLOW-FROM webvisor.com'

# Send Mail settings
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_USE_TLS = True
EMAIL_HOST = EMAIL_HOST
EMAIL_HOST_USER = EMAIL_USER
EMAIL_HOST_PASSWORD = EMAIL_PASSWORD
EMAIL_PORT = EMAIL_PORT

AWS_ACCESS_KEY_ID = aws_access_key_id
AWS_SECRET_ACCESS_KEY = aws_secret_access_key
AWS_STORAGE_BUCKET_NAME = aws_bucket

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'
DEFAULT_FILE_STORAGE = 'part4_project.storage_backends.MediaStorage'


FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'console': {
#             'format': '%(name)-12s %(levelname)-8s %(message)s'
#         },
#         'file': {
#             'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
#         }
#     },
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#             'formatter': 'console'
#         },
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'formatter': 'file',
#             'filename': 'debug.log'
#         }
#     },
#     'loggers': {
#         '': {
#             'level': 'DEBUG',
#             'handlers': ['console', 'file']
#         }
#     }
# }
