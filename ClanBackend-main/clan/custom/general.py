import os
from pathlib import Path

DEBUG = os.environ.get("DEBUG", False)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
APP_SCHEME=''
SECRET_KEY = os.environ.get("SECRET_KEY","django-insecure-lz3a&twztkdv2dq5q*4jq^g*j^mp#3kt*qj_@!8**kgkoqlinb")
ALLOWED_HOSTS = ['*']
AUTH_USER_MODEL = 'users.User'
WSGI_APPLICATION = 'clan.wsgi.application'
ASGI_APPLICATION = "clan.asgi.application"
ROOT_URLCONF = 'clan.urls'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SOFT_DELETE=True


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
]


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": os.environ.get("REDIS_URL_CACHE", "redis://localhost:6379/4"),
    }
}


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


SWAGGER_SETTINGS = {
    # 'SECURITY_DEFINITIONS': {
    #     'Bearer': {
    #         'type': 'apiKey',
    #         'name': 'Authorization',
    #         'in': 'header'
    #     }
    # }
}