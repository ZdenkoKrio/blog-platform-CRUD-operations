from django.test import TestCase
from django.contrib.auth.models import User
from ..models import UserProfile


class UserProfileModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_profile_creation(self):
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertEqual(self.user.profile.bio, None)

    def test_default_profile_picture(self):
        profile = self.user.profile
        self.assertEqual(profile.profile_picture, 'profile_pics/default.png')

    def test_update_profile(self):
        profile = self.user.profile
        profile.bio = 'This is a test bio.'
        profile.website = 'https://example.com'
        profile.save()

        updated_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(updated_profile.bio, 'This is a test bio.')
        self.assertEqual(updated_profile.website, 'https://example.com')

    def test_profile_string_representation(self):
        # Test the string representation of the profile
        profile = self.user.profile
        self.assertEqual(str(profile), 'testuser Profile')