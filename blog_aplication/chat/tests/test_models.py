from django.test import TestCase
from django.contrib.auth.models import User
from posts.models import Category
from chat.models import RoomMessage, PrivateChat, PrivateMessage


class RoomMessageModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.category = Category.objects.create(name="Technology", description="All about tech")
        self.message = RoomMessage.objects.create(
            category=self.category,
            sender=self.user,
            message="Hello World!"
        )

    def test_room_message_creation(self):
        self.assertEqual(self.message.category, self.category)
        self.assertEqual(self.message.sender, self.user)
        self.assertEqual(self.message.message, "Hello World!")
        self.assertIsNotNone(self.message.timestamp)

    def test_room_message_str(self):
        self.assertEqual(str(self.message), "testuser: Hello World!")


class PrivateChatModelTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password1")
        self.user2 = User.objects.create_user(username="user2", password="password2")
        self.private_chat = PrivateChat.objects.create(user1=self.user1, user2=self.user2)

    def test_private_chat_creation(self):
        self.assertEqual(self.private_chat.user1, self.user1)
        self.assertEqual(self.private_chat.user2, self.user2)
        self.assertIsNotNone(self.private_chat.created_at)

    def test_private_chat_str(self):
        self.assertEqual(str(self.private_chat), "Chat between user1 and user2")


class PrivateMessageModelTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password1")
        self.user2 = User.objects.create_user(username="user2", password="password2")
        self.private_chat = PrivateChat.objects.create(user1=self.user1, user2=self.user2)
        self.private_message = PrivateMessage.objects.create(
            chat=self.private_chat,
            sender=self.user1,
            message="Hello, User2!"
        )

    def test_private_message_creation(self):
        self.assertEqual(self.private_message.chat, self.private_chat)
        self.assertEqual(self.private_message.sender, self.user1)
        self.assertEqual(self.private_message.message, "Hello, User2!")
        self.assertIsNotNone(self.private_message.timestamp)

    def test_private_message_str(self):
        self.assertEqual(str(self.private_message), "Message from user1 in chat 1")