from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Post, Category


class PostDetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

        try:
            self.category = Category.objects.create(name='Category1', description='Description 1')
        except Exception as e:
            print(f"Error creating category: {e}")

        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post.',
            author=self.user,
            category=self.category
        )

        self.url = reverse('post-detail', kwargs={'pk': self.post.pk})

    def test_post_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_detail_view_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'posts/post_detail.html')

    def test_post_detail_view_context(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context['object'], self.post)

    def test_post_detail_view_content(self):
        response = self.client.get(self.url)
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.content)
        self.assertContains(response, self.post.author.username)

    def test_post_detail_view_invalid_post(self):
        invalid_url = reverse('post-detail', kwargs={'pk': 9999})
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, 404)