from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
)


class TestPostURLs(SimpleTestCase):

    def test_post_list_url_is_resolved(self):
        url = reverse('post-list')
        self.assertEqual(resolve(url).func.view_class, PostListView)

    def test_post_detail_url_is_resolved(self):
        url = reverse('post-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, PostDetailView)

    def test_post_create_url_is_resolved(self):
        url = reverse('post-create')
        self.assertEqual(resolve(url).func.view_class, PostCreateView)

    def test_post_update_url_is_resolved(self):
        url = reverse('post-edit', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, PostUpdateView)

    def test_post_delete_url_is_resolved(self):
        url = reverse('post-delete', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, PostDeleteView)