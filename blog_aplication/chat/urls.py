from django.urls import path
from .views import (ChatRoomView,
                    ChatMessagesView,
                    PrivateChatListView,
                    PrivateChatDetailView,
                    ChatRoomListView, PrivateChatStartView)


urlpatterns = [
    path('chat-list/', ChatRoomListView.as_view(), name='chat-room-list'),
    path('private-chat-list/', PrivateChatListView.as_view(), name='private-chat-list'),

    path('private-chat/<int:pk>/', PrivateChatDetailView.as_view(), name='private-chat-detail'),

    path('<str:category_name>/', ChatRoomView.as_view(), name='chat-room'),

    path('<str:chat_type>/<str:chat_id>/messages/', ChatMessagesView.as_view(), name='chat-room-messages'),
    path('start-chat/<int:user_id>/', PrivateChatStartView.as_view(), name='private-chat-start'),
]