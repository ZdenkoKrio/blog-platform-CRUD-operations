from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from posts.models import Post
from comments.models import Comment


class CommentCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.post = Post.objects.create(title='Test Post', content='Test content', author=self.user)
        self.url = reverse('comments:comment-create', kwargs={'post_id': self.post.id})

    def test_comment_create_view_redirects_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_comment_create_view_renders_form_for_logged_in_user(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'comments/comment_form.html')

    def test_comment_creation(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(self.url, {'content': 'Test comment'})
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().content, 'Test comment')
        self.assertRedirects(response, self.post.get_absolute_url())


"""class CommentDeleteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.other_user = User.objects.create_user(username='otheruser', password='password')
        self.post = Post.objects.create(title='Test Post', content='Test content', author=self.user)
        self.comment = Comment.objects.create(content='Test comment', author=self.user, post=self.post)
        self.url = reverse('comments:comment-delete', kwargs={'pk': self.comment.id})

    def test_comment_delete_view_redirects_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_comment_delete_view_forbidden_for_non_author(self):
        self.client.login(username='otheruser', password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_comment_delete_view_allows_author(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(self.url)
        self.assertEqual(Comment.objects.count(), 0)
        self.assertRedirects(response, reverse('post-detail', kwargs={'pk': self.post.id}))"""