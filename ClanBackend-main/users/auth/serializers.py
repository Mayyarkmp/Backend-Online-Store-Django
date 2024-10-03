from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError
from django.core.cache import cache
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from users.utils import check_username, check_user_email, check_user_phone_number, send_otp

from users.auth import google, apple
from users.auth.register import register_social_user
from users.models import User


class RegisterStaffClanSerializer(serializers.ModelSerializer):
    """
        Register Staff Clan
    """
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30, required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    phone_number = PhoneNumberField(required=False, allow_blank=True)
    username = serializers.CharField(min_length=5, required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['email', "username", 'phone_number', 'password', 'first_name', 'last_name']

    def validate(self, attrs):
        email = attrs.get('email')
        phone_number = attrs.get('phone_number')
        username = attrs.get('username')


        if not email and not phone_number:
            raise ValidationError("Please provide either email or phone number.")

        if check_user_email(email) or check_user_phone_number(phone_number):
            raise ValidationError("User already registered")

        if check_username(username):
            raise ValidationError("Username already taken")


        return attrs

    def create(self, validated_data):
        try:
            user = User.objects.create_user(**validated_data)
        except Exception:
            return Response({"message": f"Error creating user"}, status=status.HTTP_400_BAD_REQUEST)

        email = validated_data.get('email')
        phone_number = validated_data.get('phone_number')

        if email:
            try:
                token_email, otp_email = send_otp(email, is_email=True)
            except Exception:
                return Response({"message": f"Error creating email token"},
                                status=status.HTTP_400_BAD_REQUEST)

        if phone_number:
            try:
                phone_number = phone_number.as_international.replace(" ", "")
                token_phone, otp_phone = send_otp(phone_number, is_email=False)
            except Exception:
                return Response({"message": f"Error creating phone token"},
                                status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "message": "User registered successfully. Please verify your account.",
            "data": {
                'email_token': token_email if email else None,
                'phone_token': token_phone if phone_number else None,
                "timeout": 120
            }
        }, status=status.HTTP_200_OK)


class PhoneAuthenticationSerializer(serializers.Serializer):
    """
        Serializer of Register or Login Customer use phone number
    """
    phone_number = PhoneNumberField()


class PhoneNumberVerificationSerializer(serializers.Serializer):
    """
    Serializer for phone number verification
    """
    phone_number = PhoneNumberField()
    otp = serializers.CharField(max_length=6)
    token = serializers.CharField()


class EmailVerificationSerializer(serializers.Serializer):
    """
        Serializer for email verification
    """
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    token = serializers.CharField(max_length=555)


class ResendOTPSerializer(serializers.Serializer):
    """
    Serializer for resending OTP to email or phone number.
    """
    email = serializers.EmailField(required=False)
    phone_number = PhoneNumberField(required=False)

    def validate(self, attrs):
        email = attrs.get('email')
        phone_number = attrs.get('phone_number')

        if not email and not phone_number:
            raise serializers.ValidationError("Please provide either email or phone number.")

        if email and phone_number:
            raise serializers.ValidationError("Provide either email or phone number, not both.")

        if email and not check_user_email(email):
            raise serializers.ValidationError("Email not registered.")

        if phone_number and not check_user_phone_number(phone_number):
            raise serializers.ValidationError("Phone number not registered.")

        return attrs


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    tokens = serializers.SerializerMethodField()
    status = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'tokens', 'status']

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])
        return user.tokens()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again.')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin.')
        if not user.is_email_verified and not user.is_phone_number_verified:
            raise AuthenticationFailed('Email or phone number is not verified.')
        if not user.is_clan and not user.is_branch:
            raise AuthenticationFailed('User does not have the required permissions.')

        attrs['user'] = user
        return attrs


class GoogleAuthSerializer(serializers.Serializer):
    id_token = serializers.CharField(required=True)


class AppleAuthSerializer(serializers.Serializer):
    id_token = serializers.CharField(required=True)


class PasswordResetOTPRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("No user is associated with this email address.")
        return email

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)

        token, otp = send_otp(email,is_email=True)

        cache.set(f"otp_{email}", otp, timeout=300)
        return user


class PasswordResetOTPConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(min_length=6, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        otp = attrs.get('otp')

        cached_otp = cache.get(f"otp_{email}")
        if cached_otp is None or cached_otp != otp:
            raise serializers.ValidationError("Invalid or expired OTP.")

        return attrs

    def save(self):
        email = self.validated_data['email']
        new_password = self.validated_data['new_password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist.")

        user.set_password(new_password)
        user.save()

        cache.delete(f"otp_{email}")

        return user


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')
