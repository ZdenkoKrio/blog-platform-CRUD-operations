from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Post, Category


class PostCreateViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

        self.category = Category.objects.create(name='Test Category', description='Category for testing')
        self.url = reverse('post-create')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('login')))

    def test_logged_in_access_create_page(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_form.html')

    def test_create_post_success(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(self.url, {
            'title': 'Test Post',
            'content': 'This is a test post.',
            'category': self.category.id
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.content, 'This is a test post.')
        self.assertEqual(post.category, self.category)
        self.assertEqual(post.author, self.user)
        self.assertRedirects(response, post.get_absolute_url())

    def test_invalid_post_creation(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(self.url, {
            'content': 'This post has no title.',
            'category': self.category.id
        })

        self.assertEqual(Post.objects.count(), 0)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_form.html')