from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from posts.models import Category


class RoomMessage(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='chat_messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.sender.username}: {self.message}"