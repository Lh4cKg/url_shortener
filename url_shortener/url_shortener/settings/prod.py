from .base import *  # noqa


ALLOWED_HOSTS = ['s.2n.ge']

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'shortenerdb',
        'USER': 'postgres',
        'PASSWORD': 'short!@#2nge43ener',
        'HOST': '127.0.0.1',
        'PORT': 5432,
    }
}

STATIC_ROOT = '/src/staticfiles'
MEDIA_ROOT = '/src/media'
