from django.test import TestCase
from django.contrib.auth.models import User
from posts.models import Post
from comments.models import Comment


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Test comment content'
        )

    def test_comment_creation(self):
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.first()
        self.assertEqual(comment.content, 'Test comment content')
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.post, self.post)

    def test_comment_string_representation(self):
        comment = Comment.objects.first()
        expected_representation = f'Comment by {self.user.username} on {self.post.title}'
        self.assertEqual(str(comment), expected_representation)

    def test_comment_auto_timestamp(self):
        self.assertIsNotNone(self.comment.created_at)