import os

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
