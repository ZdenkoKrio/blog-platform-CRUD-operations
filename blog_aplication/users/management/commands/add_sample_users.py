from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Adds sample users if they do not already exist'

    def handle(self, *args, **kwargs):
        sample_users = [
            {'username': 'user1', 'email': 'user1@example.com', 'password': 'password123'},
            {'username': 'user2', 'email': 'user2@example.com', 'password': 'password123'},
            {'username': 'user3', 'email': 'user3@example.com', 'password': 'password123'},
        ]

        for user_data in sample_users:
            if not User.objects.filter(username=user_data['username']).exists():
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password=user_data['password']
                )
                self.stdout.write(self.style.SUCCESS(f"User '{user.username}' created."))
            else:
                self.stdout.write(self.style.WARNING(f"User '{user_data['username']}' already exists."))
