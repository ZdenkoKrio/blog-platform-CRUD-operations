from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Post, Category


class PostUpdateViewTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username='author', password='password')
        self.other_user = User.objects.create_user(username='other_user', password='password')

        self.category = Category.objects.create(name='Test Category', description='Test Description')
        self.post = Post.objects.create(
            title='Original Title',
            content='Original Content.',
            author=self.author,
            category=self.category,
        )

        self.update_url = reverse('post-edit', kwargs={'pk': self.post.pk})

    def test_update_post_as_author(self):
        self.client.login(username='author', password='password')

        response = self.client.post(self.update_url, {
            'title': 'Updated Title',
            'content': 'Updated Content.',
            'category': self.category.id,
        })

        self.assertRedirects(response, self.post.get_absolute_url())
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Title')
        self.assertEqual(self.post.content, 'Updated Content.')

    def test_update_post_as_other_user(self):
        self.client.login(username='other_user', password='password')

        response = self.client.post(self.update_url, {
            'title': 'Malicious Update',
            'content': 'This should not work.',
            'category': self.category.id,
        })

        self.assertEqual(response.status_code, 403)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Original Title')
        self.assertEqual(self.post.content, 'Original Content.')

    def test_update_post_as_anonymous(self):
        response = self.client.post(self.update_url, {
            'title': 'Anonymous Update',
            'content': 'This should not work.',
            'category': self.category.id,
        })

        self.assertRedirects(response, f"{reverse('login')}?next={self.update_url}")
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Original Title')
        self.assertEqual(self.post.content, 'Original Content.')

    def test_update_post_template(self):
        self.client.login(username='author', password='password')

        response = self.client.get(self.update_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_form.html')