from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from posts.models import Category
from chat.models import PrivateChat


class ChatRoomListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.category1 = Category.objects.create(name='Category 1', description='Description 1')
        self.category2 = Category.objects.create(name='Category 2', description='Description 2')
        self.url = reverse('chat:chat-room-list')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{reverse('login')}?next={self.url}")

    def test_logged_in_user_can_access_chat_room_list(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/chat_list.html')
        self.assertContains(response, 'Category 1')
        self.assertContains(response, 'Category 2')


class PrivateChatListViewTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.user3 = User.objects.create_user(username='user3', password='password')
        self.chat1 = PrivateChat.objects.create(user1=self.user1, user2=self.user2)
        self.chat2 = PrivateChat.objects.create(user1=self.user2, user2=self.user3)
        self.url = reverse('chat:private-chat-list')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{reverse('users:login')}?next={self.url}")

    def test_logged_in_user_can_access_private_chat_list(self):
        self.client.login(username='user1', password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/chat_list.html')
        self.assertContains(response, 'user2')

    def test_private_chat_list_shows_only_related_chats(self):
        self.client.login(username='user1', password='password')
        response = self.client.get(self.url)
        self.assertContains(response, 'user2')
        self.assertNotContains(response, 'user3')