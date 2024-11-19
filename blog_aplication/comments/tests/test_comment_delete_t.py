from django.test import TestCase
from django.contrib.auth.models import User
from posts.models import Post
from comments.models import Comment
from django.urls import reverse


class CommentDeleteTemplateTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.post = Post.objects.create(title='Test Post', content='Test Content', author=self.user)
        self.comment = Comment.objects.create(content='Test Comment', author=self.user, post=self.post)
        self.url = reverse('comment-delete', kwargs={'pk': self.comment.pk})

    def test_comment_delete_template_rendered(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'comments/comment_confirm_delete.html')
        self.assertContains(response, "Are you sure you want to delete this comment?")
        self.assertContains(response, "Yes, delete")
        self.assertContains(response, "Cancel")
        self.assertContains(response, self.comment.post.get_absolute_url)

    def test_template_contains_csrf_token(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.url)
        self.assertContains(response, 'csrfmiddlewaretoken')