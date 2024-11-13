from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from posts.models import Post
from comments.models import Comment


class Command(BaseCommand):
    help = 'Adds sample comments to posts if they do not already exist'

    def handle(self, *args, **kwargs):
        if not Post.objects.exists():
            self.stdout.write(self.style.ERROR("No posts found. Please create some posts first."))
            return

        sample_comments = [
            {"content": "Great post!", "username": "user1"},
            {"content": "Very informative, thanks!", "username": "user2"},
            {"content": "I enjoyed reading this.", "username": "user3"},
        ]

        posts = Post.objects.all()
        for i, post in enumerate(posts):
            comment_data = sample_comments[i % len(sample_comments)]
            author = User.objects.filter(username=comment_data["username"]).first()

            if author and not Comment.objects.filter(post=post, author=author, content=comment_data["content"]).exists():
                Comment.objects.create(
                    post=post,
                    author=author,
                    content=comment_data["content"]
                )
                self.stdout.write(self.style.SUCCESS(f"Comment added to '{post.title}' by '{author.username}'."))
            else:
                self.stdout.write(self.style.WARNING(f"Comment already exists or author '{comment_data['username']}' not found."))