import environ

from .base import *

env = environ.Env()

DEBUG = True
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True
# tail -f /tmp/debug.log .
LOGGING = {'version': 1, 'disable_existing_loggers': False, 'handlers': {
    'file': {'level': 'DEBUG', 'class': 'logging.FileHandler',
             'filename': '/tmp/debug.log', }, }, 'loggers': {
    'django': {'handlers': ['file'], 'level': 'DEBUG',
               'propagate': True, }, }, }
SECRET_KEY = env(
    'DJANGO_SECRET_KEY',
    default='django-insecure-=3js',
)

ALLOWED_HOSTS = ['*']
# ALLOWED_HOSTS = ("localhost", "0.0.0.0", "127.0.0.1")

INSTALLED_APPS += ['debug_toolbar']

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': ['debug_toolbar.panels.redirects.RedirectsPanel'],
    'SHOW_TEMPLATE_CONTEXT': True,
}

INTERNAL_IPS = ['127.0.0.1', '10.129.0.8']

INSTALLED_APPS += ['django_extensions']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DB', default='foodgram'),
        'USER': env('POSTGRES_USER', default='foodgram_user'),
        'PASSWORD': env('POSTGRES_PASSWORD', default='333333'),
        'HOST': env('POSTGRES_HOST', default='postgres'),
        'PORT': env('POSTGRES_PORT', default='5432'),
    }
}
