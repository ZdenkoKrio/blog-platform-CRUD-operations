from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Category, Post
from django.utils.translation import activate


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Technology",
            description="All about technology"
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Technology")
        self.assertEqual(self.category.description, "All about technology")

    def test_category_str_representation(self):
        self.assertEqual(str(self.category), "Technology")


class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.category = Category.objects.create(
            name="Music",
            description="All about music"
        )
        self.post = Post.objects.create(
            title="Test Post",
            content="This is a test post.",
            author=self.user,
            category=self.category
        )

    def test_post_creation(self):
        self.assertEqual(self.post.title, "Test Post")
        self.assertEqual(self.post.content, "This is a test post.")
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.category, self.category)

    def test_post_str_representation(self):
        self.assertEqual(str(self.post), "Test Post")

    def test_post_get_absolute_url(self):
        activate('en')
        self.assertEqual(self.post.get_absolute_url(), f"/en/posts/{self.post.pk}/")

    def test_post_category_null(self):
        self.post.category = None
        self.post.save()
        self.assertIsNone(self.post.category)

    def test_post_author_deleted(self):
        self.user.delete()
        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(pk=self.post.pk)