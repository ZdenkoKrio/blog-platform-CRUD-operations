from django.test import SimpleTestCase
from django.urls import reverse, resolve
from comments.views import CommentCreateView, CommentDeleteView


class CommentURLsTest(SimpleTestCase):
    def test_comment_create_url_resolves(self):
        url = reverse('comments:comment-create', kwargs={'post_id': 1})
        self.assertEqual(resolve(url).func.view_class, CommentCreateView)

    def test_comment_delete_url_resolves(self):
        url = reverse('comments:comment-delete', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, CommentDeleteView)