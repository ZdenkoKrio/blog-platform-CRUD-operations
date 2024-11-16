from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from ..models import RoomMessage, PrivateChat, PrivateMessage
from posts.models import Category


class ChatMessagesView(ListView):
    template_name = None
    context_object_name = "messages"

    def get_queryset(self):
        chat_type = self.kwargs.get('chat_type')  # "group" or "private"
        offset = int(self.request.GET.get('offset', 0))
        limit = 10

        if chat_type == "group":
            category_name = self.kwargs.get('chat_id')
            category = get_object_or_404(Category, name=category_name)
            return RoomMessage.objects.filter(category=category).order_by('-timestamp')[offset:offset + limit]

        elif chat_type == "private":
            chat_id = self.kwargs.get('chat_id')
            chat = get_object_or_404(PrivateChat, pk=chat_id)
            return PrivateMessage.objects.filter(chat=chat).order_by('-timestamp')[offset:offset + limit]
        else:
            return []

    def render_to_response(self, context, **response_kwargs):
        messages = self.get_queryset()

        data = [
            {
                'sender': message.sender.username,
                'message': message.message,
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }
            for message in messages
        ]
        return JsonResponse({'messages': data})