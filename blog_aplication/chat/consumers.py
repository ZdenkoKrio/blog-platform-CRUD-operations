import json
from asgiref.sync import sync_to_async
from django.db import IntegrityError
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import RoomMessage, PrivateChat, PrivateMessage
from posts.models import Category


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_type = self.scope['url_route']['kwargs']['chat_type']  # "group" or "private"
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']

        if self.chat_type == "group":
            self.room_group_name = f"group_chat_{self.chat_id}"

        elif self.chat_type == "private":
            self.room_group_name = f"private_chat_{self.chat_id}"

        else:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
         if hasattr(self, 'room_group_name') and self.room_group_name:
            try:
                await self.channel_layer.group_discard(
                    self.room_group_name,
                    self.channel_name
                )

            except Exception as e:
                print(f"Error while disconnecting from {self.chat_type} chat {self.chat_id}: {e}")

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = self.scope['user'].username

        if self.chat_type == "group":
            await self.save_group_message(message)
        elif self.chat_type == "private":
            await self.save_private_message(message)

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
    def save_group_message(self, message):
        try:
            category = Category.objects.get(name=self.chat_id)  # id is name of category
            user = self.scope['user']
            if not user.is_authenticated:
                raise ValueError("User must be authenticated to send messages.")

            RoomMessage.objects.create(
                category=category,
                sender=user,
                message=message
            )
        except Category.DoesNotExist:
            print(f"Error: Category '{self.chat_id}' does not exist.")
        except IntegrityError as e:
            print(f"Error saving group message: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    @sync_to_async
    def save_private_message(self, message):
        try:
            chat = PrivateChat.objects.get(id=self.chat_id)
            user = self.scope['user']
            if not user.is_authenticated:
                raise ValueError("User must be authenticated to send messages.")

            PrivateMessage.objects.create(
                chat=chat,
                sender=user,
                content=message
            )
        except PrivateChat.DoesNotExist:
            print(f"Error: PrivateChat with id '{self.chat_id}' does not exist.")
        except IntegrityError as e:
            print(f"Error saving private message: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

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