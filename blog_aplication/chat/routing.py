from django.urls import path
from .consumers import ChatConsumer


websocket_urlpatterns = [
    path('ws/chat/<str:category_name>/', ChatConsumer.as_asgi()),
]