import json
from django.utils import timezone
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chat_messages.models import (
    Message,
    MessageParticipants,
    Participant,
    MessageReceiver,
)
from django.contrib.auth.models import User
from chat_messages.utility.notification import create_chat_message_notification
from climateconnect_api.utility.notification import (
    create_user_notification,
    create_email_notification,
)


class DirectMessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_anonymous:
            await self.channel_layer.group_add(
                "user-" + str(self.user.id), self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        self.user = self.scope["user"]
        await self.channel_layer.group_discard(
            "user-" + str(self.user.id), self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        chat_uuid = text_data_json["chat_uuid"]
        self.user = self.scope["user"]
        # Send message to room group
        message_object = await self.new_message(chat_uuid, self.user, message)
        for receiver in message_object["receivers"]:
            await self.channel_layer.group_send(
                "user-" + str(receiver.id),
                {
                    "type": "chat_message",
                    "message": message,
                    "chat_uuid": chat_uuid,
                    "message_id": message_object["message"].id,
                },
            )

    @database_sync_to_async
    def _get_chat(self, chat_uuid):
        """Get chat by UUID - wrapped for async safety."""
        try:
            return MessageParticipants.objects.get(chat_uuid=chat_uuid)
        except MessageParticipants.DoesNotExist:
            return None

    @database_sync_to_async
    def _get_receivers(self, chat):
        """Get active receivers for a chat - wrapped for async safety."""
        receiver_user_ids = Participant.objects.filter(
            chat=chat, is_active=True
        ).values_list("user", flat=True)
        return list(User.objects.filter(id__in=receiver_user_ids))

    @database_sync_to_async
    def _create_message(self, message_content, user, chat):
        """Create message and update chat - wrapped for async safety."""
        message = Message.objects.create(
            content=message_content,
            sender=user,
            message_participant=chat,
            sent_at=timezone.now(),
        )
        chat.last_message_at = timezone.now()
        chat.save()
        return message

    @database_sync_to_async
    def _create_notification(self, chat):
        """Create chat notification - wrapped for async safety."""
        return create_chat_message_notification(chat)

    @database_sync_to_async
    def _create_receiver_notifications(self, receiver, message, chat, message_content, user, notification):
        """Create receiver record and notifications - wrapped for async safety."""
        MessageReceiver.objects.create(receiver=receiver, message=message)
        create_email_notification(receiver, chat, message_content, user, notification)
        create_user_notification(receiver, notification)

    async def new_message(self, chat_uuid, user, message_content):
        chat = await self._get_chat(chat_uuid)
        if chat is None:
            return {"message": None, "receivers": []}
        
        receiver_users = await self._get_receivers(chat)
        message = await self._create_message(message_content, user, chat)
        notification = await self._create_notification(chat)
        
        for receiver in receiver_users:
            if receiver.id != user.id:
                await self._create_receiver_notifications(
                    receiver, message, chat, message_content, user, notification
                )
        
        return {"message": message, "receivers": receiver_users}

    # Receive message from room group
    async def chat_message(self, event):
        if not self.user.is_anonymous:
            message = event["message"]
            # Send message to WebSocket
            await self.send(
                text_data=json.dumps(
                    {
                        "message": message,
                        "type": event["type"],
                        "chat_uuid": event["chat_uuid"],
                        "message_id": event["message_id"],
                    }
                )
            )

    async def notification(self, event):
        if not self.user.is_anonymous:
            await self.send(text_data=json.dumps({"type": event["type"]}))
