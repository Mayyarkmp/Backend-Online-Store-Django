import os

from celery import Celery
from django.conf import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clan.settings")

app = Celery("clan")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.update(
    broker_connection_retry_on_startup=True,
)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
