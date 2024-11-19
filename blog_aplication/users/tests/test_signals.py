from django.test import TestCase
from django.contrib.auth.models import User
from users.models import UserProfile

class TestUserProfileSignals(TestCase):

    def test_user_profile_created_on_user_creation(self):
        # Vytvorenie používateľa
        user = User.objects.create_user(username='testuser', password='testpassword')
        # Overenie, že profil bol automaticky vytvorený
        self.assertTrue(UserProfile.objects.filter(user=user).exists())

    def test_user_profile_saved_on_user_save(self):
        # Vytvorenie používateľa
        user = User.objects.create_user(username='testuser', password='testpassword')
        user.profile.bio = "Updated bio"
        user.save()
        # Overenie, že profil bol uložený s aktualizovanými údajmi
        self.assertEqual(UserProfile.objects.get(user=user).bio, "Updated bio")