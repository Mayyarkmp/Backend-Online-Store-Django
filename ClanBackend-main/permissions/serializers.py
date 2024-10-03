from rest_framework.serializers import ModelSerializer

from .models import Role, Permission, AssignedBranches
from permissions.dynamic import DynamicFieldsModelSerializer
from parler_rest.serializers import TranslatedFieldsField


class AssignedBranchesSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = AssignedBranches
        fields = '__all__'


class PermissionSerializer(DynamicFieldsModelSerializer):
    translations = TranslatedFieldsField(shared_model=Permission)

    class Meta:
        model = Permission
        fields = '__all__'


class RoleSerializer(DynamicFieldsModelSerializer):
    translations = TranslatedFieldsField(shared_model=Role)

    class Meta:
        model = Role
        fields = '__all__'
