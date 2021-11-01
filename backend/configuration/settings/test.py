import environ

from .base import *

env = environ.Env()

SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="fewsdgrbnfthyjyutykj3546434XdTLqpf0sb1yiz6hLlrsispZkWu",
)

TEST_RUNNER = "django.test.runner.DiscoverRunner"

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
