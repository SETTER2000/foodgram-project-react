import environ

from .base import *

env = environ.Env()

DEBUG = True

SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="django-insecure-=3js",
)

ALLOWED_HOSTS = ("*",)
# ALLOWED_HOSTS = ("localhost", "0.0.0.0", "127.0.0.1")

INSTALLED_APPS += ["debug_toolbar"]

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}

INTERNAL_IPS = ["*"]
# INTERNAL_IPS = ["127.0.0.1", "10.129.0.8", "10.0.2.2"]

INSTALLED_APPS += ["django_extensions"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB", default="foodgram_user"),
        "USER": env("POSTGRES_USER", default="foodgram_user"),
        "PASSWORD": env("POSTGRES_PASSWORD", default="333333"),
        "HOST": env("POSTGRES_HOST", default="postgres"),
        "PORT": env("POSTGRES_PORT", default="5432"),
    }
}
