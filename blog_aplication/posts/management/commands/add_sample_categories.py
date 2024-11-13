from django.core.management.base import BaseCommand
from posts.models import Category


class Command(BaseCommand):
    help = 'Adds sample data for categories and posts'

    def handle(self, *args, **kwargs):
        categories_data = [
            {"name": "Technology", "description": "Posts about the latest in technology."},
            {"name": "Health", "description": "Posts about health and wellness."},
            {"name": "Lifestyle", "description": "Posts on lifestyle and personal growth."},
            {"name": "Travel", "description": "Stories and tips about traveling."},
            {"name": "Education", "description": "Resources and insights into education and learning."}
        ]

        for category_data in categories_data:
            category, created = Category.objects.get_or_create(**category_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Category '{category.name}' created."))
            else:
                self.stdout.write(self.style.WARNING(f"Category '{category.name}' already exists."))
