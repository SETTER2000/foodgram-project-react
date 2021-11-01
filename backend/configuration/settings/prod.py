import os

from .base import *
from .base import env

DEBUG = False

SECRET_KEY = env(
    'DJANGO_SECRET_KEY',
    default='django-insecure-=3js',
)
# SECRET_KEY = env('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = [
    '127.0.0.1',
    '178.154.193.199',
    'kino2000.ru',
    'www.kino2000.ru',
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': os.environ.get('POSTGRES_PORT'),
    }
}
