from django.views.generic import TemplateView


class ChatRoomView(TemplateView):
    template_name = "chat/base_chat.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Room: {kwargs.get('category_name')}"
        context['chat_id'] = kwargs.get('category_name')
        context['chat_type'] = "group"
        return context
