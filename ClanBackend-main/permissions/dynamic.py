from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.contenttypes.models import ContentType
from permissions.models import Permission, Role, AssignedBranches
from rest_framework import serializers, viewsets
from parler_rest.serializers import TranslatableModelSerializer


class DynamicPermission(BasePermission):
    message = _('You do not have permission to perform this action.')

    def has_permission(self, request, view):
        jwt_auth = JWTAuthentication()
        try:
            user, token = jwt_auth.authenticate(request)
        except Exception:
            return False

        if not user or not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        model = view.queryset.model if hasattr(view, 'queryset') else None

        if not model:
            return False

        content_type = ContentType.objects.get_for_model(model)

        if self.check_user_permissions(user, content_type, request):
            return True

        if self.check_role_permissions(user, content_type, request):
            return True

        return False

    def check_user_permissions(self, user, content_type, request):
        user_permissions = user.permissions.filter(content_type=content_type)

        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return user_permissions.filter(view=True).exists()
        elif request.method in ('POST',):
            return user_permissions.filter(create=True).exists()
        elif request.method in ('PUT', 'PATCH'):
            return user_permissions.filter(edit=True).exists()
        elif request.method == 'DELETE':
            return user_permissions.filter(delete=True).exists()

        return False

    def check_role_permissions(self, user, content_type, request):
        try:
            assign_branches = AssignedBranches.objects.get(user=user)
            roles = Role.objects.filter(
                permissions__content_type=content_type,
                permissions__level__in=[Role.Levels.ALL, Role.Levels.ASSIGNED_BRANCHES],
                uid__in=assign_branches.branches.values_list('role__uid', flat=True)
            ).distinct()
        except AssignedBranches.DoesNotExist:
            return False

        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return any(role.permissions.filter(view=True).exists() for role in roles)
        elif request.method in ('POST',):
            return any(role.permissions.filter(create=True).exists() for role in roles)
        elif request.method in ('PUT', 'PATCH'):
            return any(role.permissions.filter(edit=True).exists() for role in roles)
        elif request.method == 'DELETE':
            return any(role.permissions.filter(delete=True).exists() for role in roles)
        return False

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class DynamicFieldsModelSerializer(TranslatableModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

        if fields and fields != '*':
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        abstract = True


class BaseModelViewSet(viewsets.ModelViewSet):
    permission_classes = [DynamicPermission]

    def get_serializer(self, *args, **kwargs):
        user = self.request.user

        content_type = ContentType.objects.get_for_model(self.get_queryset().model)

        permissions = Permission.objects.filter(user=user, content_type=content_type).first()

        if self.action in ['list', 'retrieve']:
            fields = permissions.view_fields if permissions else []
        elif self.action == 'create':
            fields = permissions.create_fields if permissions else []
        elif self.action in ['update', 'partial_update']:
            fields = permissions.edit_fields if permissions else []
        else:
            fields = []

        if '*' in fields:
            fields = '*'
        kwargs['fields'] = fields
        return super().get_serializer(*args, **kwargs)
