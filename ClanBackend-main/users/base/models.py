import uuid
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, )
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from core.base.models import TimeStampedModel

class UserManager(BaseUserManager):
    def create_user(self, email=None, username=None, password=None, **extra_fields):
        if not email and not extra_fields["phone_number"]:
            raise ValueError('Users must have either an email address or a phone number')

        email = self.normalize_email(email) if email else None
        username = username if username else email.split('@')[
            0] if email else f'user_{uuid.uuid4().hex[:8]}' if email else extra_fields[
            'phone_number'].as_international.replace(" ", "")

        user = self.model(
            email=email,
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    @staticmethod
    def email_validator(email):
        try:
            validate_email(email)
        except:
            ValueError(_("Please enter a valid email address"))

    def all(self, with_unactive=False):
        if with_unactive:
            return self.filter(is_deleted=False)
        return self.filter(is_deleted=False, is_active=True)

    def inactive(self):
        return self.filter(is_deleted=False, is_active=False)




class AbstractUser(AbstractBaseUser,TimeStampedModel):
    class AuthProviders(models.TextChoices):
        APPLE = "APPLE"
        GOOGLE = "GOOGLE"
        EMAIL = "EMAIL"
        PHONE = "PHONE"

    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    email_authentication = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    phone_number = PhoneNumberField(blank=True)
    phone_number_authentication = models.BooleanField(default=False)
    phone_verification_token = models.UUIDField(default=uuid.uuid4, editable=False, null=True, blank=True)
    is_phone_number_verified = models.BooleanField(default=False)
    google_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    google_authentication = models.BooleanField(default=False)
    apple_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    apple_authentication = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    data_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    tow_factor_authentication = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    def __str__(self):
        return self.email or self.username or self.phone_number.as_international

    @property
    def auth_providers(self):
        providers = []
        if self.email_authentication:
            providers.append("EMAIL")

        if self.phone_number_authentication:
            providers.append("PHONE_NUMBER")

        if self.google_authentication:
            providers.append("GOOGLE")

        if self.apple_authentication:
            providers.append("APPLE")

        return providers

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def link_google_account(self, google_data):
        if not self.google_id:
            self.google_id = google_data['id']
            self.google_authentication = True
            self.save()
        return self

    def link_apple_account(self, apple_data):
        if not self.apple_id:
            self.apple_id = apple_data['id']
            self.apple_authentication = True
            self.save()
        return self

    def link_phone_account(self, phone_number):
        if not self.phone_number:
            self.phone_number = phone_number

            self.save()
        return self

    def verified_phone_number(self):
        self.is_verified_phone_number = True
        self.phone_number_authentication = True
        return self

    @property
    def full_name(self):
        if self.last_name is not None:
            return self.first_name + ' ' + self.last_name
        else:
            return self.first_name

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()
        return self

    class Meta:
        abstract = True
