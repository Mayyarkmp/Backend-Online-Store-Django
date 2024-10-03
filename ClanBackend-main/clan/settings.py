from .custom import *
import dotenv


INSTALLED_APPS = [
    "daphne",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django.contrib.gis",
    "parler",
    "parler_rest",
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    'rest_framework_simplejwt.token_blacklist',
    'rest_framework_word_filter',
    'corsheaders',
    'drf_yasg',
    "phonenumber_field",
    'cities_light',
    'django_user_agents',
    'storages',
    'minio_storage'
]

PROJECT_APPS = [
    'users',
    'core',
    'core.media',
    'core.settings',
    'permissions',
    'branches',
    'products',
    'chat'
]


INSTALLED_APPS += PROJECT_APPS
