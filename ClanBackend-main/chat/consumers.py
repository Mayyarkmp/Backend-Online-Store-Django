import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Message
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime
from celery import shared_task
from .tasks import create_message_task 
User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            self.user = self.scope["user"]
            self.room_uuid = self.scope['url_route']['kwargs']['room_uuid']
            self.room_group_name = f'chat_{self.room_uuid}'

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json["action"]

        if action == "create":
            message_type = text_data_json['type']
            content = text_data_json['content']
            room = await self.get_room()
            sender = self.user
            receiver = await self.get_reciever(room, sender)

            message = await self.create_message(
                room, sender, receiver, content, message_type
            )

        elif action in ["receiving", "reading", "editing"]:
            message_uuid = text_data_json['uuid']

            if action == "editing":
                content = text_data_json["content"]
                message = await self.edit_message(message_uuid, content)
            else:
                message = await self.update_message(message_uuid, action)

        # إرسال الرسالة المحدثة إلى مجموعة WebSocket
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))

    @database_sync_to_async
    def get_room(self):
        return Room.objects.get(uuid=self.room_uuid)
    
    @database_sync_to_async
    def get_reciever(self, room, sender):
        return room.members.exclude(id=sender.id).first()

    @database_sync_to_async
    def edit_message(self, uuid, content):
        try:
            message = Message.objects.get(uuid=uuid)
            old_content = json.loads(message.old_content or '{"messages": []}')
            old_messages = old_content["messages"] + [message.message]
            message.old_content = json.dumps({
                "last_update": datetime.now().isoformat(),
                "messages": old_messages
            })
            message.message = content
            message.editing_datetime = datetime.now()
            message.is_edited = True
            message.is_read = False
            message.is_received = False
            message.is_sent = True
            message.save()
            return {
                "uuid": str(message.uuid),
                "is_edited": message.is_edited,
                "is_read": message.is_read,
                "is_sent": message.is_sent,
                "is_received": message.is_received,
                "editing_datetime": message.editing_datetime.isoformat()
            }
        except Message.DoesNotExist:
            return {
                "uuid": str(uuid.uuid4()),
                "error": "can't find message",
            }

    @database_sync_to_async
    def update_message(self, uuid, action):
        try:
            message = Message.objects.get(uuid=uuid)
            if message and self.user == message.receiver:
                if action == "reading":
                    message.is_received = True
                    message.receiving_datetime = datetime.now()
                    message.is_read = True
                    message.reading_datetime = datetime.now()
                    message.save()
                    return {
                        "uuid": str(message.uuid),
                        "is_read": message.is_read,
                        "is_received": message.is_received,
                        "receiving_datetime": message.receiving_datetime.isoformat(),
                        "reading_datetime": message.reading_datetime.isoformat(),
                    }
                elif action == "receiving":
                    message.is_received = True
                    message.receiving_datetime = datetime.now()
                    message.save()
                    return {
                        "uuid": str(message.uuid),
                        "is_received": message.is_received,
                        "receiving_datetime": message.receiving_datetime.isoformat(),
                    }
        except Message.DoesNotExist:
            return {
                "error": "Can't find message",
            }

    @database_sync_to_async
    def create_message(self, room, sender, receiver, content, message_type):
        message = Message.objects.create(
            room=room,
            sender=sender,
            receiver=receiver,
            message=content,
            type=message_type,
            sending_datetime=timezone.now(),
            is_sent=True
        )
        return {
            "uuid": str(message.uuid),
            "is_sent": message.is_sent,
            "content": message.message,
            "sender": str(message.sender.id),
            "receiver": str(message.receiver.id),
            "timestamp": message.timestamp.isoformat(),
            "type": message.type,
        }
