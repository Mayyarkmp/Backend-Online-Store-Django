import os
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ.get("POSTGRES_DB", "postgres"),
        'USER': os.environ.get("POSTGRES_USER", "postgres"),
        'PASSWORD': os.environ.get("POSTGRES_PASSWORD", "postgres"),
        'HOST': os.environ.get("POSTGRES_HOST", "localhost"),
        'PORT': int(os.environ.get("POSTGRES_PORT",5432)),
    }
}

