from django.urls import path
from .views import ChatRoomView, ChatRoomMessagesView, chat_room_list


urlpatterns = [
    path('chat-list/', chat_room_list, name='chat-room-list'),
    path('<str:category_name>/', ChatRoomView.as_view(), name='chat-room'),
    path('<str:category_name>/messages/', ChatRoomMessagesView.as_view(), name='chat-room-messages'),
]