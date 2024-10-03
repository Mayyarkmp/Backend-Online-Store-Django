import uuid
import os
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.deconstruct import deconstructible
from PIL import Image
from ..base.models import TimeStampedModel


@deconstructible
class PathAndRename:
    def __init__(self, sub_path='media'):
        self.sub_path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = f"default.{ext}"
        return os.path.join(self.sub_path, str(instance.uid), filename)





class Media(TimeStampedModel):
    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to=PathAndRename)
    file_type = models.CharField(max_length=20)


    def get_related_models(self):
        related_models = []
        content_type = ContentType.objects.get_for_model(self)
        for relation in self._meta.related_objects:
            model = relation.related_model
            if model._meta.app_label == content_type.app_label:
                related_models.append(model._meta.verbose_name)
        return related_models

    def __str__(self):
        return str(self.uid)
