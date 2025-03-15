# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from asgiref.sync import database_sync_to_async
import logging

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            logging.info("Connecting to WebSocket...")
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = f'chat_{self.room_name}'

            # Join the room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            logger.info(f"User connected to room {self.room_name}")
            await self.accept()
        except Exception as e:
            logger.info(f"Error during WebSocket connection: {e}")
            await self.close()

    async def disconnect(self, close_code):
        logger.info("Disconnecting from WebSocket...")
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        logger.info(f"User disconnected from room {self.room_name}")

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = text_data_json['user']

        logger.info(f"Received message from user {user}: {message}")
        
        # Save the message to the database
        await database_sync_to_async(self.save_message)(message, user)
        logger.info(f"Message saved to database: {message}")

        # Send message to the room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user,
            }
        )
        logger.info(f"Message sent to room {self.room_name}")

    async def chat_message(self, event):
        message = event['message']
        user = event['user']

        # Send the message to the WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
        }))
        logger.info(f"Message sent to WebSocket: {message}")

    def save_message(self, message, user):
        Message.objects.create(message=message, room_name=self.room_name, user=user)
        logger.info(f"Message saved to database: {message}")