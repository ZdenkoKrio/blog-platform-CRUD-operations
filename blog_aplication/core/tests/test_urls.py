from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import HomeView, AboutView, ContactView


class TestUrls(SimpleTestCase):
    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func.view_class, HomeView)

    def test_about_url_resolves(self):
        url = reverse('about')
        self.assertEqual(resolve(url).func.view_class, AboutView)

    def test_contact_url_resolves(self):
        url = reverse('contact')
        self.assertEqual(resolve(url).func.view_class, ContactView)
