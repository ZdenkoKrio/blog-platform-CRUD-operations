from django.test import TestCase
from django.contrib.auth.models import User
from posts.models import Post
from django.urls import reverse
from comments.models import Comment


class CommentCreateTemplateTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.post = Post.objects.create(title='Test Post', content='Test Content', author=self.user)
        self.url = reverse('comment-create', kwargs={'post_id': self.post.pk})

    def test_comment_create_template_rendered(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'comments/comment_form.html')
        self.assertContains(response, "Add a Comment")
        self.assertContains(response, "Submit Comment")

    def test_template_contains_csrf_token(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_comment_form_submission(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(self.url, {'content': 'This is a test comment'})
        self.assertEqual(response.status_code, 302)  # Should redirect to the post detail page
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().content, 'This is a test comment')
        self.assertEqual(Comment.objects.first().post, self.post)
        self.assertEqual(Comment.objects.first().author, self.user)