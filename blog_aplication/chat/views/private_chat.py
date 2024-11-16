from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, View
from ..models import PrivateChat, PrivateMessage
from django.contrib.auth.models import User


class PrivateChatDetailView(DetailView):
    model = PrivateChat
    template_name = 'chat/base_chat.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chat = self.get_object()
        context['title'] = f"Chat with {chat.user1.username if chat.user1 != self.request.user else chat.user2.username}"
        context['chat_id'] = chat.id
        context['chat_type'] = "private"
        return context

    def post(self, request, pk):
        chat = get_object_or_404(PrivateChat, pk=pk)
        content = request.POST.get('message')

        if content:
            PrivateMessage.objects.create(
                chat=chat,
                sender=request.user,
                content=content
            )
        return redirect('private-chat-detail', pk=chat.id)


class PrivateChatStartView(View):
    def get(self, request, user_id):
        other_user = get_object_or_404(User, pk=user_id)

        if other_user == request.user:
            return redirect('user-profile', pk=request.user.pk)

        chat, created = PrivateChat.objects.get_or_create(
            user1=min(request.user, other_user, key=lambda u: u.pk),
            user2=max(request.user, other_user, key=lambda u: u.pk)
        )

        return redirect('private-chat-detail', pk=chat.pk)