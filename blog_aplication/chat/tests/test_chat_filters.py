from django.test import TestCase
from django.contrib.auth.models import User
from chat.models import PrivateChat
from chat.templatetags.chat_filters import other_user


class OtherUserFilterTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password1")
        self.user2 = User.objects.create_user(username="user2", password="password2")
        self.chat = PrivateChat.objects.create(user1=self.user1, user2=self.user2)

    def test_other_user_returns_correct_username_for_user1(self):
        result = other_user(self.chat, self.user1)
        self.assertEqual(result, self.user2.username)

    def test_other_user_returns_correct_username_for_user2(self):
        result = other_user(self.chat, self.user2)
        self.assertEqual(result, self.user1.username)