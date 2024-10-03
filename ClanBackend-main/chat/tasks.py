from celery import shared_task
from .models import Room, Message
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

@shared_task
def create_message_task(room_id, sender_id, receiver_id, content, message_type):
    room = Room.objects.get(id=room_id)
    sender = User.objects.get(id=sender_id)
    receiver = User.objects.get(id=receiver_id)
    message = Message.objects.create(
        room=room,
        sender=sender,
        receiver=receiver,
        message=content,
        type=message_type,
        sending_datetime=timezone.now(),
        is_sent=True
    )
    return message
