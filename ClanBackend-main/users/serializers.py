from rest_framework import serializers
from permissions.dynamic import DynamicFieldsModelSerializer
from users.models import User, UserAddress, UserInfo, CardID
from parler_rest.serializers import TranslatedFieldsField


class UserSerializer(DynamicFieldsModelSerializer):
    password = serializers.CharField(write_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_verified = serializers.BooleanField(read_only=True)
    is_verified_phone_number = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = '__all__'


class UserAddressSerializer(DynamicFieldsModelSerializer):
    translations = TranslatedFieldsField(shared_model=UserAddress)
    class Meta:
        model = UserAddress
        fields = '__all__'


class UserInfoSerializer(DynamicFieldsModelSerializer):
    translations = TranslatedFieldsField(shared_model=UserInfo)

    class Meta:
        model = UserInfo
        fields = "__all__"


class CardIDSerializer(DynamicFieldsModelSerializer):
    translations = TranslatedFieldsField(shared_model=CardID)

    class Meta:
        model = CardID
        fields = "__all__"

