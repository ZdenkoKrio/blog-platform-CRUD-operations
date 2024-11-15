from django.shortcuts import render, get_object_or_404
from posts.models import Category


def chat_room_list(request):
    categories = Category.objects.all()
    return render(request, 'chat/chat_room_list.html', {'categories': categories})
