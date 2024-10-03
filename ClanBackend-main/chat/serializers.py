from rest_framework import serializers
from .models import Room

class RoomSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True,)
    class Meta:
        model = Room
        fields = ('members','uuid')