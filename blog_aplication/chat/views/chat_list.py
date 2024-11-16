from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from ..models import PrivateChat
from posts.models import Category


class ChatRoomListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'chat/chat_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.all()


class PrivateChatListView(LoginRequiredMixin, ListView):
    model = PrivateChat
    template_name = 'chat/chat_list.html'
    context_object_name = 'chats'

    def get_queryset(self):
        return PrivateChat.objects.filter(
            Q(user1=self.request.user) | Q(user2=self.request.user)
        )