from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from chat.models import PrivateChat
from posts.models import Category


class ChatTemplateTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password1")
        self.user2 = User.objects.create_user(username="user2", password="password2")
        self.category = Category.objects.create(name="TestCategory", description="Test Description")
        self.private_chat = PrivateChat.objects.create(user1=self.user1, user2=self.user2)

    def test_group_chat_template_renders_correctly(self):
        self.client.login(username="user1", password="password1")
        response = self.client.get(reverse('chat:chat-room', kwargs={'category_name': self.category.name}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/base_chat.html')
        self.assertContains(response, "Chat: Room: TestCategory")
        self.assertContains(response, 'data-chat-type="group"')
        self.assertContains(response, f'data-chat-id="{self.category.name}"')

    def test_private_chat_template_renders_correctly(self):
        self.client.login(username="user1", password="password1")
        response = self.client.get(reverse('chat:private-chat-detail', kwargs={'pk': self.private_chat.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/base_chat.html')
        self.assertContains(response, f"Chat with {self.user2.username}")
        self.assertContains(response, 'data-chat-type="private"')
        self.assertContains(response, f'data-chat-id="{self.private_chat.pk}"')

    def test_chat_template_includes_static_scripts(self):
        self.client.login(username="user1", password="password1")
        response = self.client.get(reverse('chat:private-chat-detail', kwargs={'pk': self.private_chat.pk}))

        self.assertContains(response, 'src="/static/js/loadOldMessages.js"')
        self.assertContains(response, 'src="/static/js/sendingMessages.js"')