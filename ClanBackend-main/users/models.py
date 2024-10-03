import uuid

from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import Group
from django.db import models
from parler.models import TranslatableModel, TranslatedFields
from users.base.models import AbstractUser, UserManager
from core.base.models import TimeStampedTranslatableModel
from django.utils.translation import gettext_lazy as _


class CustomUserManager(UserManager):
    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError("Password should not be none")
        user = self.create_user(username=username, email=email, password=password)
        user.is_superuser = True
        user.is_clan = True
        user.status = user.Status.ACTIVE
        user.type = user.Type.CLAN
        user.clan_job = user.ClanJobs.ADMIN
        user.is_email_verified = True
        user.save()
        return user

    def reviewing(self):
        return self.filter(status=User.Status.REVIEWING)

    def blocked(self):
        return self.filter(status=User.Status.BLOCKED)

    def customers(self):
        return self.filter(type=User.Type.CUSTOMER)

    def clans(self, job=None):
        if job is None:
            return self.filter(type=User.Type.CLAN, is_clan=True)
        return self.filter(type=User.Type.CLAN, job=job)

    def branches(self, job=None):
        if job is None:
            return self.filter(type=User.Type.BRANCH)
        return self.filter(type=User.Type.BRANCH, job=job)

    def for_branch(self, branch):
        if branch is None:
            return ValueError("Branch cannot be None")
        return self.filter(type=User.Type.BRANCH, branch=branch, is_branch=True)

    def deliveries(self):
        return self.filter(branch_job=User.BranchJobs.DELIVERY, is_delivery=True)

    def preparers(self):
        return self.filter(branch_job=User.BranchJobs.PREPARER, is_preparer=True)


class User(AbstractUser, PermissionsMixin):
    class Type(models.TextChoices):
        CUSTOMER = "CUSTOMER", _("Customer")
        CLAN = "CLAN", _("Clan")
        BRANCH = "BRANCH", _("Branch")

    class ClanJobs(models.TextChoices):
        NONE = "NONE", _("None")
        ADMIN = "ADMIN", _("Administrator")
        STAFF = "STAFF", _("Staff")

    class BranchJobs(models.TextChoices):
        NONE = "NONE", _("None")
        MANAGER = "MANAGER", _("Branch Manager")
        ADMIN = "ADMIN", _("Branch Administrator")
        STAFF = "STAFF", _("Branch Staff")
        DELIVERY = "DELIVERY", _("Delivery")
        PREPARER = "PREPARER", _("Preparer")

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", _("Active")
        INACTIVE = "INACTIVE", _("Inactive")
        REVIEWING = "REVIEWING", _("Reviewing")
        BLOCKED = "BLOCKED", _("Blocked")

    objects = CustomUserManager()

    type = models.CharField(
        _("Type"), choices=Type.choices, default=Type.CUSTOMER, max_length=50
    )
    clan_job = models.CharField(
        _("Job in clan"), choices=ClanJobs.choices, default=ClanJobs.NONE, max_length=50
    )
    branch_job = models.CharField(
        _("Job in branch"),
        choices=BranchJobs.choices,
        default=BranchJobs.NONE,
        max_length=50,
    )

    status = models.CharField(
        _("Account Status"),
        choices=Status.choices,
        default=Status.ACTIVE,
        max_length=50,
    )

    is_customer = models.BooleanField(_("Is customer"), default=False)
    is_clan = models.BooleanField(_("Is clan"), default=False)
    is_branch = models.BooleanField(_("Is Branch"), default=False)

    is_admin = models.BooleanField(_("Is administrator"), default=False)
    is_staff = models.BooleanField(_("Is staff"), default=False)
    is_delivery = models.BooleanField(_("Is delivery"), default=False)
    is_preparer = models.BooleanField(_("Is preparer"), default=False)

    permissions = models.ManyToManyField(
        "permissions.Permission",
        verbose_name=_("User Permissions"),
        blank=True,
        related_name="users",
    )
    branch = models.ForeignKey(
        "branches.Branch",
        related_name="staffs",
        verbose_name=_("User Branch"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.email or self.username or self.phone_number.as_international

    def set_for_clan(self, job="NONE"):
        self.set_for(user_type=self.Type.BRANCH, job=job)

    def set_for_branch(self, job="NONE"):
        self.set_for(user_type=self.Type.BRANCH, job=job)

    def set_customer(self):
        self.set_for(user_type=self.Type.CUSTOMER)

    def set_for(self, user_type="CUSTOMER", job="NONE"):
        self.is_customer = False
        self.is_clan = False
        self.is_branch = False
        self.is_admin = False
        self.is_staff = False
        self.is_delivery = False
        self.is_preparer = False

        self.clan_job = "NONE"
        self.branch_job = "NONE"

        self.type = user_type
        if user_type == "CUSTOMER":
            self.is_customer = True
            self.type = self.Type.CUSTOMER
        if user_type == "CLAN":
            self.is_clan = True
            self.clan_job = job
        if user_type == "BRANCH":
            self.is_branch = True
            self.branch_job = job

        self.save()


class CustomerManager(UserManager):
    def get_queryset(self):
        return self.filter(is_customer=True, type=self.Type.CUSTOMER)


class Customer(User):
    objects = CustomerManager()

    def save(self, *args, **kwargs):
        self.type = self.Type.CUSTOMER
        self.is_customer = True
        self.status = self.Status.ACTIVE
        super(Customer, self).save(*args, **kwargs)

    class Meta:
        proxy = True


class ClanUserManager(UserManager):
    def get_queryset(self):
        return self.filter(is_clan=True, is_staff=True)


class ClanUser(User):
    objects = ClanUserManager()

    def save(self, *args, **kwargs):
        if self.type == self.Type.CLAN:
            self.status = self.Status.REVIEWING

        super(ClanUser, self).save(*args, **kwargs)

    class Meta:
        proxy = True


class UserInfo(models.Model):
    uid = models.UUIDField(_("UID"), default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="info", verbose_name=_("User")
    )
    date_of_birth = models.DateField(_("Date of Birth"), blank=True, null=True)
    gender = models.CharField(
        _("Gender"), choices=(("F", _("Female")), ("M", _("Male"))), max_length=1
    )

    def __str__(self):
        return f"{self.user.first_name}'s info"


class UserAddress(TimeStampedTranslatableModel):
    uid = models.UUIDField(_("UID"), default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="addresses", verbose_name=_("User")
    )
    translations = TranslatedFields(
        name=models.CharField(_("Address Name"), max_length=255),
        street_name=models.CharField(_("Street Name"), max_length=255),
    )
    street_number = models.CharField(_("Street Number"), max_length=10)
    country = models.ForeignKey(
        "settings.Country", on_delete=models.CASCADE, verbose_name=_("Country")
    )
    city = models.ForeignKey(
        "settings.City", on_delete=models.CASCADE, verbose_name=_("City")
    )
    region = models.ForeignKey(
        "settings.Region", on_delete=models.CASCADE, verbose_name=_("Region")
    )
    postal_code = models.CharField(_("Postal Code"), max_length=20)
    location = gis_models.PointField(
        _("Location"), geography=True, blank=True, null=True
    )
    is_default = models.BooleanField(_("Is Default"), default=False)

    def __str__(self):
        return f"{self.user.username} - {self.street_name}, {self.city}"

    def save(self, *args, **kwargs):
        if self.is_default:
            UserAddress.objects.filter(user=self.user, is_default=True).update(
                is_default=False
            )
        if not self.name:
            self.name = self.street_name + " " + self.city.name
        super().save(*args, **kwargs)

    def set_location(self, latitude, longitude):
        self.location = Point(longitude, latitude)
        self.save()


class CardID(TimeStampedTranslatableModel):
    uid = models.UUIDField(_("UID"), default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="card", verbose_name=_("User")
    )
    translations = TranslatedFields(
        first_name=models.CharField(_("First Name"), max_length=20),
        second_name=models.CharField(
            _("Second Name"), max_length=20, blank=True, null=True
        ),
        third_name=models.CharField(
            _("Third Name"), max_length=20, blank=True, null=True
        ),
        family_name=models.CharField(_("Family Name"), max_length=20),
    )
    gender = models.CharField(
        _("Gender"), choices=(("F", _("Female")), ("M", _("Male"))), max_length=1
    )
    date_of_birth = models.DateField(_("Date of Birth"), blank=True, null=True)
    place_of_birth = models.CharField(
        _("Place of Birth"), max_length=20, blank=True, null=True
    )
    date_of_end = models.DateField(_("Date of End"), blank=True, null=True)
    number = models.CharField(_("Card Number"), max_length=20, unique=True)
    front_image = models.ImageField(
        _("Front Image"), upload_to="cards/", blank=True, null=True
    )
    back_image = models.ImageField(
        _("Back Image"), upload_to="cards/", blank=True, null=True
    )

    def __str__(self):
        return f"{self.first_name} {self.family_name}"
