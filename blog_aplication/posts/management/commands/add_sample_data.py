from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from posts.models import Category, Post


class Command(BaseCommand):
    help = 'Adds sample data for categories and posts'

    def handle(self, *args, **kwargs):
        try:
            author = User.objects.get(id=1)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR("User with ID 1 does not exist. Please create a user with ID 1 first."))
            return

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

        posts_data = [
            {
                "title": "The Future of AI in Technology",
                "content": "Artificial intelligence is rapidly advancing, affecting all areas of technology.",
                "category": Category.objects.get(name="Technology")
            },
            {
                "title": "Top 10 Health Tips for 2024",
                "content": "Stay healthy and fit with these top 10 health tips for the coming year.",
                "category": Category.objects.get(name="Health")
            },
            {
                "title": "Minimalist Lifestyle: A Guide to Simple Living",
                "content": "Minimalism is more than a trend; it's a lifestyle that promotes peace and simplicity.",
                "category": Category.objects.get(name="Lifestyle")
            },
            {
                "title": "Best Travel Destinations for 2024",
                "content": "Explore the best travel destinations around the world for your 2024 adventures.",
                "category": Category.objects.get(name="Travel")
            },
            {
                "title": "Learning in the Digital Age",
                "content": "Digital tools and online resources are reshaping the educational landscape.",
                "category": Category.objects.get(name="Education")
            },
        ]

        for post_data in posts_data:
            post, created = Post.objects.get_or_create(author=author, **post_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Post '{post.title}' created."))
            else:
                self.stdout.write(self.style.WARNING(f"Post '{post.title}' already exists."))