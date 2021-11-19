import os
from datetime import timedelta

import dotenv

# import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration
#
# sentry_sdk.init(
#     dsn='https://9ebbbce0f7244178ac893020081ff7df@o960815.ingest.sentry.io/6010342',
#     integrations=[DjangoIntegration()],
#     traces_sample_rate=1.0,
#     send_default_pii=True
# )

dotenv.load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.getenv('SECRET_KEY', 'DEFAULT')

DEFAULT_FROM_EMAIL = 'admin@example.com'
EVD = '-пусто-'
DEBUG = False
# DEBUG = os.environ.get('DJANGO_DEBUG')

# ALLOWED_HOSTS = [host for host in os.environ.get('ALLOWED_HOSTS')]
ALLOWED_HOSTS = ['*']

FONT_PDF = 'api/fonts/Oswald.ttf'
# FONT_PDF = os.environ.get('FONT_PDF')


# SUB_DIR_RECIPES = os.environ.get('SUB_DIR_RECIPES')
SUB_DIR_RECIPES = 'recipes'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'corsheaders',
    'django_filters',
    'users',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'foodgram.urls'

# TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
# TEMPLATES_DIR = os.path.join(BASE_DIR, 'frontend/../../frontend/build')

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

WSGI_APPLICATION = 'foodgram.wsgi.application'

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': os.environ.get('DB_ENGINE'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD')
    }
}

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

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
# STATICFILES_DIRS = ((os.path.join(BASE_DIR,
#                                   'frontend/build/../../frontend/build/static')),)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/api/.*$'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

AUTH_USER_MODEL = 'users.User'
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    # 'DEFAULT_RENDERER_CLASSES': [
    #     'rest_framework.renderers.JSONRenderer',
    # ],
    # 'DEFAULT_PARSER_CLASSES': [
    #     'rest_framework.parsers.JSONParser',
    # ],
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 6,
}

DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': '#/password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': '#/username/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': '#/activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    'SERIALIZERS': {},
    'LOGIN_FIELD': 'email',
    'USER_ID_FIELD': 'id',
}

SILENCED_SYSTEM_CHECKS = ['auth.E003', 'auth.W004']

SIMPLE_JWT = {'ACCESS_TOKEN_LIFETIME': timedelta(days=30)}

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'

EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'sent_emails')

AUTH_USER_MODEL = 'users.User'

ROLES_PERMISSIONS = {
    'Users': {
        'user': (None,),
        'moderator': (None,),
        'anon': ('POST',),
    },
    'Reviews': {
        'user': ('GET', 'POST'),
        'moderator': ('GET', 'PATCH', 'DELETE', 'POST', 'PUT'),
        'anon': ('GET',),
    },
    'Shopping': {
        'user': ('GET', 'POST'),
        'moderator': ('GET', 'PATCH', 'DELETE', 'POST', 'PUT'),
        'anon': ('GET',),
    },
    'Categories': {
        'user': ('GET',),
        'moderator': ('GET',),
        'anon': ('GET',),
    },
    'Tag': {
        'user': ('GET',),
        'moderator': ('GET'),
        'anon': ('GET',),
    },
    'Titles': {
        'user': ('GET',),
        'moderator': ('GET',),
        'anon': ('GET',),
    }, }
