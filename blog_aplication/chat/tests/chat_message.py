from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from chat.models import RoomMessage, PrivateChat, PrivateMessage
from posts.models import Category


class ChatMessagesViewTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password")
        self.user2 = User.objects.create_user(username="user2", password="password")

        self.category = Category.objects.create(name="TestCategory", description="Test description")
        self.room_message1 = RoomMessage.objects.create(category=self.category, sender=self.user1,
                                                        message="Room message 1")
        self.room_message2 = RoomMessage.objects.create(category=self.category, sender=self.user2,
                                                        message="Room message 2")

        self.private_chat = PrivateChat.objects.create(user1=self.user1, user2=self.user2)
        self.private_message1 = PrivateMessage.objects.create(chat=self.private_chat, sender=self.user1,
                                                              message="Private message 1")
        self.private_message2 = PrivateMessage.objects.create(chat=self.private_chat, sender=self.user2,
                                                              message="Private message 2")

    def test_group_chat_messages(self):
        url = reverse('chat:chat-room-messages', kwargs={'chat_type': 'group', 'chat_id': self.category.name})
        response = self.client.get(url, {'offset': 0})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['messages']), 2)
        self.assertIn("Room message 1", [msg['message'] for msg in response.json()['messages']])
        self.assertIn("Room message 2", [msg['message'] for msg in response.json()['messages']])

    def test_private_chat_messages(self):
        url = reverse('chat:chat-room-messages', kwargs={'chat_type': 'private', 'chat_id': self.private_chat.id})
        response = self.client.get(url, {'offset': 0})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['messages']), 2)
        self.assertIn("Private message 1", [msg['message'] for msg in response.json()['messages']])
        self.assertIn("Private message 2", [msg['message'] for msg in response.json()['messages']])

    def test_invalid_chat_type(self):
        url = reverse('chat:chat-room-messages', kwargs={'chat_type': 'invalid', 'chat_id': 'random_id'})
        response = self.client.get(url, {'offset': 0})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['messages']), 0)

    def test_group_chat_pagination(self):
        url = reverse('chat:chat-room-messages', kwargs={'chat_type': 'group', 'chat_id': self.category.name})
        response = self.client.get(url, {'offset': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['messages']), 1)
        self.assertIn("Room message 1", [msg['message'] for msg in response.json()['messages']])

    def test_private_chat_pagination(self):
        url = reverse('chat:chat-room-messages', kwargs={'chat_type': 'private', 'chat_id': self.private_chat.id})
        response = self.client.get(url, {'offset': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['messages']), 1)
        self.assertIn("Private message 1", [msg['message'] for msg in response.json()['messages']])