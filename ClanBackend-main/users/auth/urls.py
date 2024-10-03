from django.urls import path
from users.auth.views import (
    LoginAPIView,
    RegisterStaffClanView,
    VerifyEmail,
    PasswordResetOTPConfirmView,
    PasswordResetOTPRequestView,
    LogoutAPIView,
    VerifyPhoneAuthentication,
    CheckUserNameView,
    ResendOTPView,
    PhoneAuthentication,
    AppleAuthView,
    GoogleAuthView
)

app_name = "auth"

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
    path('register/clan/', RegisterStaffClanView.as_view(), name='register_staff_clan'),
    path('verify-email/', VerifyEmail.as_view(), name='verify_email'),
    path('password-reset/request/', PasswordResetOTPRequestView.as_view(), name='password_reset_request'),
    path('password-reset/confirsm/', PasswordResetOTPConfirmView.as_view(), name='password_reset_confirm'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('phone/verify/', VerifyPhoneAuthentication.as_view(), name='verify_phone'),
    path('check-username/', CheckUserNameView.as_view(), name='check_username'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend_otp'),
    path('phone/', PhoneAuthentication.as_view(), name='phone'),
    path('google/', GoogleAuthView.as_view(), name='google'),
    path('apple/', AppleAuthView.as_view(), name='apple'),
]