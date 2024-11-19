from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from chat.models import PrivateChat
from posts.models import Category


class ChatOverviewTemplateTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password1")
        self.user2 = User.objects.create_user(username="user2", password="password2")
        self.category1 = Category.objects.create(name="TestCategory1", description="Description1")
        self.category2 = Category.objects.create(name="TestCategory2", description="Description2")
        self.private_chat = PrivateChat.objects.create(user1=self.user1, user2=self.user2)

    def test_chat_overview_with_categories(self):
        self.client.login(username="user1", password="password1")
        response = self.client.get(reverse('chat:chat-room-list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/chat_list.html')
        self.assertContains(response, "Chat Rooms")
        self.assertContains(response, "Room: TestCategory1")
        self.assertContains(response, "Room: TestCategory2")

    def test_chat_overview_with_private_chats(self):
        self.client.login(username="user1", password="password1")
        response = self.client.get(reverse('chat:private-chat-list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/chat_list.html')
        self.assertContains(response, "Private Chats")
        self.assertContains(response, f"Chat with {self.user2.username}")

    def test_chat_overview_no_items(self):
        self.client.login(username="user2", password="password2")
        response = self.client.get(reverse('chat-room-list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/chat_list.html')
        self.assertContains(response, "No items to display.")
