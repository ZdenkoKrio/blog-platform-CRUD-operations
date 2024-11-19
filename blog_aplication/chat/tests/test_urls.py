from django.test import SimpleTestCase
from django.urls import reverse, resolve
from chat.views import (
    ChatRoomView,
    ChatMessagesView,
    PrivateChatListView,
    PrivateChatDetailView,
    ChatRoomListView,
    PrivateChatStartView,
)


class ChatURLsTestCase(SimpleTestCase):
    def test_chat_room_list_url(self):
        url = reverse('chat:chat-room-list')
        self.assertEqual(resolve(url).func.view_class, ChatRoomListView)

    def test_private_chat_list_url(self):
        url = reverse('chat:private-chat-list')
        self.assertEqual(resolve(url).func.view_class, PrivateChatListView)

    def test_private_chat_detail_url(self):
        url = reverse('chat:private-chat-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, PrivateChatDetailView)

    def test_chat_room_url(self):
        url = reverse('chat:chat-room', kwargs={'category_name': 'Technology'})
        self.assertEqual(resolve(url).func.view_class, ChatRoomView)

    def test_chat_messages_url(self):
        url = reverse('chat:chat-room-messages', kwargs={'chat_type': 'group', 'chat_id': '123'})
        self.assertEqual(resolve(url).func.view_class, ChatMessagesView)

    def test_private_chat_start_url(self):
        url = reverse('chat:private-chat-start', kwargs={'user_id': 2})
        self.assertEqual(resolve(url).func.view_class, PrivateChatStartView)