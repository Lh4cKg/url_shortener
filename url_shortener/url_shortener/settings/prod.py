from .base import *  # noqa


ALLOWED_HOSTS = ['go.2n.ge']

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'shortenerdb',
        'USER': 'shortener_user',
        'PASSWORD': 'short!@#2nge43ener',
        'HOST': 'pgdb',
        'PORT': 5432,
    }
}

STATIC_ROOT = '/src/staticfiles'
MEDIA_ROOT = '/src/media'
