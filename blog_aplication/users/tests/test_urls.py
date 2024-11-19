from django.test import SimpleTestCase
from django.urls import reverse, resolve
from users.views import RegisterView, UserProfileView, UserProfileUpdateView
from django.contrib.auth.views import LoginView, LogoutView


class TestUsersUrls(SimpleTestCase):

    def test_login_url_resolves(self):
        url = reverse('users:login')
        self.assertEqual(resolve(url).func.view_class, LoginView)

    def test_logout_url_resolves(self):
        url = reverse('users:logout')
        self.assertEqual(resolve(url).func.view_class, LogoutView)

    def test_register_url_resolves(self):
        url = reverse('users:register')
        self.assertEqual(resolve(url).func.view_class, RegisterView)

    def test_user_profile_url_resolves(self):
        url = reverse('users:user-profile', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, UserProfileView)

    def test_user_profile_from_post_url_resolves(self):
        url = reverse('users:user-profile-from-post', kwargs={'post_id': 1})
        self.assertEqual(resolve(url).func.view_class, UserProfileView)

    def test_user_profile_edit_url_resolves(self):
        url = reverse('users:profile-edit')
        self.assertEqual(resolve(url).func.view_class, UserProfileUpdateView)