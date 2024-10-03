from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from .models import Room
from .serializers import RoomSerializer

class RoomViewSet(ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Room.objects.all()
    serializer_class = RoomSerializer