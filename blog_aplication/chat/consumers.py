import json
from asgiref.sync import sync_to_async
from django.db import IntegrityError
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import RoomMessage
from posts.models import Category


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.category_name = self.scope['url_route']['kwargs']['category_name']
        self.room_group_name = f'chat_{self.category_name}'

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
        data = json.loads(text_data)
        message = data['message']
        username = self.scope['user'].username

        # async saving to db - IMPORTANT!
        await self.save_message(message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'timestamp': await self.get_timestamp()
            }
        )

    @sync_to_async
    def save_message(self, message):
        try:
            category = Category.objects.get(name=self.category_name)

            user = self.scope['user']
            if not user.is_authenticated:
                raise ValueError("User must be authenticated to send messages.")

            chat_message = RoomMessage.objects.create(
                category=category,
                sender=user,
                message=message
            )
            return chat_message

        except Category.DoesNotExist:
            print(f"Error: Category '{self.category_name}' does not exist.")
            return None

        except IntegrityError as e:
            print(f"Error saving message: {e}")
            return None

        except ValueError as e:
            print(f"Authentication error: {e}")
            return None

        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    @sync_to_async
    def get_timestamp(self):
        from django.utils.timezone import now
        return now().strftime('%Y-%m-%d %H:%M:%S')

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        timestamp = event['timestamp']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'timestamp': timestamp
        }))


