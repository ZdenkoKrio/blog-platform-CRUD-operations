from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from chat.models import PrivateChat, PrivateMessage


class PrivateChatDetailViewTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password1")
        self.user2 = User.objects.create_user(username="user2", password="password2")
        self.client.login(username="user1", password="password1")
        self.chat = PrivateChat.objects.create(user1=self.user1, user2=self.user2)
        self.url = reverse('chat:private-chat-detail', kwargs={'pk': self.chat.pk})

    def test_private_chat_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_private_chat_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'chat/base_chat.html')

    def test_private_chat_context(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context['title'], f"Chat with {self.user2.username}")
        self.assertEqual(response.context['chat_id'], self.chat.pk)
        self.assertEqual(response.context['chat_type'], "private")

    def test_post_message(self):
        response = self.client.post(self.url, {'message': 'Hello, User2!'})
        self.assertEqual(PrivateMessage.objects.count(), 1)
        self.assertEqual(PrivateMessage.objects.first().content, 'Hello, User2!')
        self.assertRedirects(response, self.url)


class PrivateChatStartViewTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password1")
        self.user2 = User.objects.create_user(username="user2", password="password2")
        self.client.login(username="user1", password="password1")
        self.url = reverse('chat:private-chat-start', kwargs={'user_id': self.user2.pk})

    def test_private_chat_start_view_redirects_to_chat(self):
        response = self.client.get(self.url)
        chat = PrivateChat.objects.get(user1=self.user1, user2=self.user2)
        self.assertRedirects(response, reverse('chat:private-chat-detail', kwargs={'pk': chat.pk}))

    def test_private_chat_start_view_creates_chat(self):
        self.client.get(self.url)
        self.assertEqual(PrivateChat.objects.count(), 1)
        chat = PrivateChat.objects.first()
        self.assertEqual(chat.user1, self.user1)
        self.assertEqual(chat.user2, self.user2)

    def test_private_chat_start_view_redirects_to_profile_if_same_user(self):
        url = reverse('chat:private-chat-start', kwargs={'user_id': self.user1.pk})
        response = self.client.get(url)
        self.assertRedirects(response, reverse('users:user-profile', kwargs={'pk': self.user1.pk}))