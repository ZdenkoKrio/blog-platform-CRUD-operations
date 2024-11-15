from django.views.generic import TemplateView, ListView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from ..models import RoomMessage
from posts.models import Category


class ChatRoomView(TemplateView):
    template_name = "chat/chat_room.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_name = kwargs.get('category_name')
        category = get_object_or_404(Category, name=category_name)
        context['category'] = category
        return context


class ChatRoomMessagesView(ListView):
    model = RoomMessage
    template_name = None
    context_object_name = "messages"

    def get_queryset(self):
        category_name = self.kwargs.get('category_name')
        category = get_object_or_404(Category, name=category_name)
        offset = int(self.request.GET.get('offset', 0))
        limit = 10

        return RoomMessage.objects.filter(category=category).order_by('-timestamp')[offset:offset + limit]

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