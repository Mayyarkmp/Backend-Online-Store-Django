import uuid

from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from parler.models import TranslatedFields

from core.base.models import TimeStampedModel, TimeStampedTranslatableModel

User = get_user_model()


class Branch(TimeStampedModel):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", _("Active")
        REVIEWING = "REVIEWING", _("Reviewing")
        INACTIVE = "INACTIVE", _("Inactive")
        BLOCKED = "BLOCKED", _("Blocked")

    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("Branch"), max_length=100)
    serial_number = models.CharField(_("Serial Number"), max_length=15)
    country = models.ForeignKey("settings.Country", on_delete=models.CASCADE)
    region = models.ForeignKey("settings.Region", on_delete=models.CASCADE)
    city = models.ForeignKey("settings.City", on_delete=models.CASCADE)

    email = models.EmailField(_("Email"), max_length=254)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="own_branches")

    location = models.PointField(_("Location"))

    license = models.CharField(_("License"), max_length=100)
    license_file = models.FileField(_("License File"), upload_to="licenses")

    commercial_register = models.CharField(_("Commercial Register"), max_length=100)
    commercial_register_file = models.FileField(_("Commercial Register"), upload_to="commercial_registers")

    tax_number = models.CharField(_("Tax Number"), max_length=100)
    tax_file = models.FileField(_("Tax File"), upload_to="tax_files")

    iban = models.CharField(_("IBAN"), max_length=100)
    iban_number = models.CharField(_("IBAN Number"), max_length=100)
    iban_file = models.FileField(_("IBAN File"), upload_to="iban_files")

    def __str__(self) -> str:
        return self.name


class Zone(TimeStampedTranslatableModel):
    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='zones')
    translations = TranslatedFields(
        name=models.CharField(_("Name"), max_length=100)
    )
    zone = models.PolygonField(_("Zone"))

    def __str__(self) -> str:
        return self.name


class BranchSetting(TimeStampedModel):
    """
    Branch Setting model
    This model contain all settings related to a branch
    """
    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    branch = models.OneToOneField(Branch, on_delete=models.CASCADE, related_name='settings')

    """       Delivery Settings    """
    schedule_delivery = models.BooleanField(_("Schedule Delivery"), default=False)
    fast_delivery = models.BooleanField(_("Fast Delivery"), default=False)
    own_delivery = models.BooleanField(_("Own Delivery"), default=False)
    delivery_company = models.BooleanField(_("Delivery Company"), default=False)

    """       End Delivery Settings    """


