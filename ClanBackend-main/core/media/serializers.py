from rest_framework import serializers

from core.media.models import Media


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ('file', 'file_type')

