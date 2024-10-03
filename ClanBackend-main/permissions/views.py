from rest_framework.viewsets import ModelViewSet
from rest_framework import status, views
from .dynamic import DynamicPermission
from .models import Role, Permission, AssignedBranches
from .serializers import PermissionSerializer, RoleSerializer




class PermissionViewSet(ModelViewSet):
    permission_classes = [DynamicPermission]
    model = Permission
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class RoleViewSet(ModelViewSet):
    permission_classes = [DynamicPermission]
    model = Role
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class TestDynamicPermission(views.APIView):
    permission_classes = [DynamicPermission]
