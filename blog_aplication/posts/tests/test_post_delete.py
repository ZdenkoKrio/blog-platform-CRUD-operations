from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Post, Category


class PostDeleteViewTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username='author', password='password')
        self.other_user = User.objects.create_user(username='other_user', password='password')

        self.category = Category.objects.create(name='Test Category', description='Test Description')
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content.',
            author=self.author,
            category=self.category,
        )

        self.delete_url = reverse('post-delete', kwargs={'pk': self.post.pk})

    def test_delete_post_as_author(self):
        self.client.login(username='author', password='password')

        response = self.client.post(self.delete_url)

        self.assertRedirects(response, reverse('post-list'))
        self.assertEqual(Post.objects.count(), 0)

    def test_delete_post_as_other_user(self):
        self.client.login(username='other_user', password='password')

        response = self.client.post(self.delete_url)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Post.objects.count(), 1)

    def test_delete_post_as_anonymous(self):
        response = self.client.post(self.delete_url)

        self.assertRedirects(response, f"{reverse('login')}?next={self.delete_url}")
        self.assertEqual(Post.objects.count(), 1)

    def test_delete_post_template(self):
        self.client.login(username='author', password='password')

        response = self.client.get(self.delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_confirm_delete.html')