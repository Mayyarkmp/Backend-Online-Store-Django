import random
import threading
from datetime import datetime, timedelta, timezone

import jwt
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.cache import cache
from chat.consumers import User


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        EmailThread(email).start()


def generate_otp():
    return str(random.randint(100000, 999999))




def send_otp_to_phone(phone_number, otp):
    # TODO: configurations send otp code 
    print(f"Sending OTP {otp} to {phone_number}")

def send_otp_to_email(phone_number, otp):
    # TODO: configurations send otp code
    print(f"Sending OTP {otp} to {phone_number}")


def send_otp(identifier, is_email=False):
    """
        Sends OTP to email or phone and returns token and OTP.
    """
    otp = generate_otp()
    token = create_verification_token(identifier, is_email)
    cache.set(f"otp_{identifier}", otp, timeout=300)

    if is_email:
        send_otp_to_email(identifier, otp)
    else:
        send_otp_to_phone(identifier, otp)

    return token, otp

def create_verification_token(primary, email=False):
    if email:
        payload = {
            'email': primary,
            'exp': datetime.now(tz=timezone.utc) + timedelta(minutes=5),
            'iat': datetime.now(tz=timezone.utc)
        }
    else:
        payload = {
            'phone_number': primary,
            'exp': datetime.now(tz=timezone.utc) + timedelta(minutes=5),
            'iat': datetime.now(tz=timezone.utc)
        }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token


def verify_token(token, email=False):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        if email:
            return payload['email']
        return payload['phone_number']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def check_username(username):
    try:
        user = User.objects.get(username=username)
        if user:
            return True
        else:
            return False
    except User.DoesNotExist:
        return False


def check_user_email(email):
    try:
        user = User.objects.get(email=email)
        if user:
            return True
        else:
            return False
    except User.DoesNotExist:
        return False


def check_user_phone_number(phone_number):
    try:
        user = User.objects.get(phone_number=phone_number)
        if user:
            return True
        else:
            return False
    except User.DoesNotExist:
        return False
