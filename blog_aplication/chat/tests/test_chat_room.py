from django.test import TestCase
from django.urls import reverse
from posts.models import Category


class ChatRoomViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="TestCategory", description="Test description")
        self.url = reverse('chat:chat-room', kwargs={'category_name': self.category.name})

    def test_chat_room_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_chat_room_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "chat/base_chat.html")

    def test_chat_room_context(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context['title'], f"Room: {self.category.name}")
        self.assertEqual(response.context['chat_id'], self.category.name)
        self.assertEqual(response.context['chat_type'], "group")

    def test_invalid_category_name(self):
        url = reverse('chat:chat-room', kwargs={'category_name': 'InvalidCategory'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['title'], "Room: InvalidCategory")
        self.assertEqual(response.context['chat_id'], "InvalidCategory")
        self.assertEqual(response.context['chat_type'], "group")