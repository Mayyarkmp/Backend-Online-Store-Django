import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from parler.models import TranslatedFields
from branches.models import Branch
from core.base.models import TimeStampedTranslatableModel
from django.contrib.auth import get_user_model

User = get_user_model()


class AssignedBranches(TimeStampedTranslatableModel):
    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    branches = models.ManyToManyField(Branch, verbose_name=_("Branches"), related_name="admins")
    user = models.OneToOneField(User, verbose_name=_("Staff"), on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.username + f' ({self.branches.count()} branch)'


class Role(TimeStampedTranslatableModel):
    class Levels(models.TextChoices):
        ALL = "ALL", _("All")
        ASSIGNED_BRANCHES = "ASSIGNED_BRANCHES", _("Assigned Branch")
        OWNER = "OWNER", _("Owner")

    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, db_index=True)
    level = models.CharField(_("Role Level"), max_length=20, choices=Levels.choices, default=Levels.OWNER, db_index=True)

    translations = TranslatedFields(
        name=models.CharField(_("Name"), max_length=255)
    )

    codename = models.SlugField(_("Code name"), unique=True, db_index=True)
    permissions = models.ManyToManyField(
        'Permission',
        verbose_name=_('permissions'),
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')


class Permission(TimeStampedTranslatableModel):
    """ Global Permissions
            for clan staffs, admins and branches owner
    """
    class Levels(models.TextChoices):
        ALL = "ALL", _("All Branches")
        ASSIGNED_BRANCHES = "ASSIGNED_BRANCHES", _("Assigned Branches")
        OWNER = "OWNER", _("Owner Branches")

    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    level = models.CharField(
        _("Permission Level"),
        max_length=20,
        choices=Levels.choices,
        default=Levels.OWNER
    )

    view = models.BooleanField(_("Can view model"), default=False)
    edit = models.BooleanField(_("Can edit model"), default=False)
    delete = models.BooleanField(_("Can delete model"), default=False)
    create = models.BooleanField(_("Can create model"), default=False)

    # select model of permissions here
    content_type = models.ForeignKey(
        ContentType,
        verbose_name=_("Type Data"),
        on_delete=models.CASCADE,
        related_name="permissions"
    )

    # if object_id is null or blank it means the permission for all objects in models
    object_id = models.CharField(_("Object"), max_length=50, null=True, blank=True)
    content_object = GenericForeignKey( 'content_type', 'object_id')

    # "*" means all fields in model (content_type)
    view_fields = models.JSONField(_("Who are fields can view ? "), null=True, blank=True)
    edit_fields = models.JSONField(_("Who are fields can edit ? "), null=True, blank=True)
    create_fields = models.JSONField(_("Who are fields can create ? "), null=True, blank=True)

    def __str__(self):
        return f'{self.content_type.name} ()'
