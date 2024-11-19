from django.test import TestCase
from django.urls import reverse
from django.utils.translation import activate
from ..models import Post, Category
from django.contrib.auth.models import User


class TemplateTestCase(TestCase):
    def setUp(self):
        activate('en')
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Test Category')
        self.post = Post.objects.create(
            title="Test Post",
            content="This is a test post.",
            author=self.user,
            category=self.category,
        )

    def test_delete_post_template(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('post-delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_confirm_delete.html')
        self.assertContains(response, 'Are you sure you want to delete')

    def test_post_detail_template(self):
        response = self.client.get(reverse('post-detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_detail.html')
        self.assertContains(response, self.post.title)
        self.assertContains(response, 'Comments')

    def test_post_form_template(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('post-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_form.html')
        self.assertContains(response, 'New Post')

        # Test edit post form
        response = self.client.get(reverse('post-edit', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_form.html')
        self.assertContains(response, 'Edit Post')

    def test_post_list_template(self):
        response = self.client.get(reverse('post-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/posts_list.html')
        self.assertContains(response, 'Blog Posts')
        self.assertContains(response, self.post.title)

    def test_localization(self):
        activate('en')
        response = self.client.get(reverse('post-list'))
        self.assertContains(response, 'Newest First')
        self.assertContains(response, 'Search posts...')

        activate('sk')
        response = self.client.get(reverse('post-list'))
        self.assertContains(response, 'Najnovšie Prvé')
        self.assertContains(response, 'Hľadať príspevky...')