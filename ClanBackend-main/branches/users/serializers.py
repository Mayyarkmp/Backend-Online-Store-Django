from rest_framework import serializers
from .models import Delivery, Preparer, Staff, Admin
from django.contrib.auth import get_user_model
from phonenumber_field.serializerfields import PhoneNumberField
User = get_user_model()


class RegisterStepOneSerializer(serializers.Serializer):
    pass


class RegisterStepTwoSerializer(serializers.Serializer):
    pass


class RegisterStepThreeSerializer(serializers.Serializer):
    pass

