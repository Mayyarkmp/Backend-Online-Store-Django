from django.db import models
from django.utils import timezone
from parler.models import TranslatableModel, TranslatedFields

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()


class TimeStampedTranslatableModel(TimeStampedModel, TranslatableModel):
    class Meta:
        abstract = True