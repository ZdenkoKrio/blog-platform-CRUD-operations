from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Post, Category


class PostListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

        self.category1 = Category.objects.create(name='Category 1', description='Description 1')
        self.category2 = Category.objects.create(name='Category 2', description='Description 2')

        self.post1 = Post.objects.create(
            title='Post 1',
            content='Content of Post 1',
            author=self.user,
            category=self.category1
        )
        self.post2 = Post.objects.create(
            title='Post 2',
            content='Content of Post 2',
            author=self.user,
            category=self.category2
        )
        self.post3 = Post.objects.create(
            title='Post 3',
            content='Content of Post 3',
            author=self.user,
            category=self.category1
        )

        self.url = reverse('post-list')

    def test_post_list_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_list_view_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'posts/posts_list.html')

    def test_post_list_view_context(self):
        response = self.client.get(self.url)
        self.assertIn('posts', response.context)
        self.assertIn('categories', response.context)
        self.assertIn('current_ordering', response.context)
        self.assertIn('current_category', response.context)
        self.assertIn('search_query', response.context)

    def test_post_list_view_displays_all_posts(self):
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['posts']), 3)

    def test_post_list_view_filter_by_category(self):
        response = self.client.get(self.url, {'category': self.category1.id})
        posts = response.context['posts']
        self.assertEqual(len(posts), 2)
        self.assertIn(self.post1, posts)
        self.assertIn(self.post3, posts)

    def test_post_list_view_search_posts(self):
        response = self.client.get(self.url, {'q': 'Post 1'})
        posts = response.context['posts']
        self.assertEqual(len(posts), 1)
        self.assertIn(self.post1, posts)

    def test_post_list_view_order_by_newest(self):
        response = self.client.get(self.url, {'ordering': 'newest'})
        posts = response.context['posts']
        self.assertEqual(posts[0], self.post3)

    def test_post_list_view_order_by_oldest(self):
        response = self.client.get(self.url, {'ordering': 'oldest'})
        posts = response.context['posts']
        self.assertEqual(posts[0], self.post1)