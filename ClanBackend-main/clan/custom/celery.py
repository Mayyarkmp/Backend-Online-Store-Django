import os

CELERY_BROKER_URL = os.environ.get('REDIS_URL_CELERY_BROKER',"redis://localhost:6379/1")
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL_CELERY_RESULT',"redis://localhost:6379/1")