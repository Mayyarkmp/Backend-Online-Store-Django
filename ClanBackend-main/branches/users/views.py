from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from branches.models import User
from branches.users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


