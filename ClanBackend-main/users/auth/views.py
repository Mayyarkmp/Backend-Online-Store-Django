import jwt
import requests
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponsePermanentRedirect
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from django_user_agents.utils import get_user_agent
from .serializers import (
    GoogleAuthSerializer,
    AppleAuthSerializer,
    PhoneNumberVerificationSerializer,
    RegisterStaffClanSerializer,
    PasswordResetOTPRequestSerializer,
    PasswordResetOTPConfirmSerializer,
    EmailVerificationSerializer,
    LoginSerializer,
    LogoutSerializer,
    PhoneAuthenticationSerializer,
    ResendOTPSerializer
)

from users.models import User
from users.utils import verify_token, check_username, send_otp
from rest_framework.authentication import BasicAuthentication

class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [settings.APP_SCHEME, 'http', 'https']


class CheckUserNameView(views.APIView):
    @swagger_auto_schema(
        operation_summary="Check User Name Availability",
        manual_parameters=[
            openapi.Parameter(
                'username', openapi.IN_QUERY, description="Username", type=openapi.TYPE_STRING,
            )
        ],
        responses={
            200: openapi.Response(
                description="Successful response",
                examples={
                    'application/json': {'username': 'newuser'}
                },
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'username': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            ),
            400: openapi.Response(
                description="Username Taken",
                examples={
                    'application/json': {'error': 'username is already taken'}
                },
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            default="username is already taken"
                        )
                    }
                )
            )
        }
    )
    def get(self, request):
        username = request.query_params.get('username', None)
        if username is None:
            return Response({'error': 'username is required'}, status=status.HTTP_400_BAD_REQUEST)

        username_already_use = check_username(username)
        if username_already_use:
            return Response({'error': 'username is already taken'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'username': username}, status=status.HTTP_200_OK)

class RegisterStaffClanView(generics.GenericAPIView):
    """
    View for registering staff or clan members
    """
    serializer_class = RegisterStaffClanSerializer


    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_creation_response = serializer.save()
            return Response({
                "message": "User registered successfully.",
                "data": user_creation_response.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "message": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class PhoneAuthentication(generics.GenericAPIView):
    serializer_class = PhoneAuthenticationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number'].as_international.replace(" ", "")
        token, otp = send_otp(phone_number, is_email=False)
        cache.set(f"otp_{phone_number}", otp, timeout=120)
        return Response({'token': token, "timeout": 120}, status=status.HTTP_200_OK)


class VerifyPhoneAuthentication(generics.GenericAPIView):
    serializer_class = PhoneNumberVerificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number'].as_international.replace(" ", "")
        otp = serializer.validated_data['otp']
        token = serializer.validated_data['token']

        verified_phone = verify_token(token)
        if verified_phone != phone_number:
            return Response({'error': 'this key is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

        stored_otp = cache.get(f"otp_{phone_number}")
        if stored_otp == otp:
            user, created = User.objects.get_or_create(
                phone_number=serializer.validated_data['phone_number']
            )
            if created:
                user.set_unusable_password()
                if not user.email:
                    user.email = phone_number + '@clan.sa'
                if not user.username:
                    user.username = phone_number
                user.phone_number_authentication = True
                user.save()

            return Response({'message': 'Successfully verified', 'is_new_user': created}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'this otp code is incorrect'}, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmail(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']
        token = serializer.validated_data['token']

        verified_email = verify_token(token, True)
        if verified_email != email:
            return Response({'error': 'this key is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

        stored_otp = cache.get(f"otp_{email}")
        if stored_otp == otp:
            user = User.objects.get(email=email)

            if user:
                user.is_verified = True
                user.email_authentication = True
                user.save()

            return Response({'message': 'Successfully verified'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'this otp code is incorrect'}, status=status.HTTP_400_BAD_REQUEST)


class ResendOTPView(generics.GenericAPIView):
    """
    View for resending OTP to email or phone number.
    """
    serializer_class = ResendOTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        phone_number = serializer.validated_data.get('phone_number')

        if email:
            try:
                token_email, otp_email = send_otp(email, is_email=True)
                return Response({
                    "message": "OTP sent to email successfully.",
                    "data": {
                        "token": token_email,
                    }
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({
                    "message": f"Error sending OTP to email: {str(e)}"
                }, status=status.HTTP_400_BAD_REQUEST)

        if phone_number:
            try:
                phone_number = phone_number.as_international.replace(" ", "")
                token_phone, otp_phone = send_otp(phone_number, is_email=False)
                return Response({
                    "message": "OTP sent to phone number successfully.",
                    "data": {
                        "token": token_phone,
                    }
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({
                    "message": f"Error sending OTP to phone number: {str(e)}"
                }, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        agent = get_user_agent(request)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user.is_customer:
            pass
        response_data = {
            'email': user.email,
            'tokens': user.tokens(),
            'status': user.status,
            'type': user.type,
            'job': user.clan_job if user.type == user.Type.CLAN else user.branch_job
        }
        return Response(response_data, status=status.HTTP_200_OK)


class PasswordResetOTPRequestView(views.APIView):
    permission_classes = [permissions.AllowAny]
    """
    View to handle password reset OTP request
    """

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetOTPRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "OTP has been sent to your email."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetOTPConfirmView(views.APIView):
    permission_classes = [permissions.AllowAny]
    """
    View to handle password reset confirmation using OTP
    """

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetOTPConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class GoogleAuthView(generics.GenericAPIView):
    serializer_class = GoogleAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            id_token = serializer.validated_data['id_token']

            google_response = requests.get(f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}")

            if google_response.status_code == 200:
                google_data = google_response.json()

                email = google_data.get('email')
                first_name = google_data.get('given_name')
                last_name = google_data.get('family_name')
                google_id = google_data.get('sub')

                user, created = User.objects.get_or_create(
                    google_id=google_id,
                    defaults={
                        'email': email,
                        'first_name': first_name,
                        'last_name': last_name,
                        'google_authentication': True,
                        'is_active': True,
                    }
                )

                if not created:
                    user.google_authentication = True
                    user.save()

                tokens = user.tokens()

                return Response({
                    "message": "Authentication successful",
                    "tokens": tokens
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid Google token"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppleAuthView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = AppleAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            id_token = serializer.validated_data['id_token']

            try:
                apple_data = jwt.decode(id_token, options={"verify_signature": False})

                email = apple_data.get('email')
                first_name = apple_data.get('given_name')
                last_name = apple_data.get('family_name')
                apple_id = apple_data.get('sub')

                user, created = User.objects.get_or_create(
                    apple_id=apple_id,
                    defaults={
                        'email': email,
                        'first_name': first_name,
                        'last_name': last_name,
                        'apple_authentication': True,
                        'is_active': True,
                    }
                )

                if not created:
                    user.apple_authentication = True
                    user.save()

                tokens = user.tokens()

                return Response({
                    "message": "Authentication successful",
                    "tokens": tokens
                }, status=status.HTTP_200_OK)
            except jwt.ExpiredSignatureError:
                return Response({"error": "Apple token has expired"}, status=status.HTTP_400_BAD_REQUEST)
            except jwt.DecodeError:
                return Response({"error": "Invalid Apple token"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClanUserStatus(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        pass
        # user = request.user
