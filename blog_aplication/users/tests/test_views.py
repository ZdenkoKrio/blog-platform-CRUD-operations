"""from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import UserProfile
from posts.models import Post
from PIL import Image
import tempfile
from django.db.models.signals import post_save
from users.signals import create_user_profile, save_user_profile
from django.core.management import call_command


class RegisterViewTest(TestCase):
    def test_register_view_get(self):
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_view_post(self):
        response = self.client.post(reverse('users:register'), {
            'username': 'testuser',
            'password1': 'securePassword123',
            'password2': 'securePassword123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())


class UserProfileUpdateViewTest(TestCase):
    def setUp(self):
        call_command('flush', verbosity=0, interactive=False)

        self.user = User.objects.create_user(username='testuser', password='securePassword123')

        existing_profile = UserProfile.objects.filter(user=self.user).first()

        if existing_profile:
            print(f"Profile already exists: {existing_profile}")
        else:
            print("No existing profile found, creating new one.")
            self.profile = UserProfile.objects.create(user=self.user, bio='Initial Bio')

        self.client.login(username='testuser', password='securePassword123')

    def test_update_view_get(self):
        response = self.client.get(reverse('users:profile-edit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile_form.html')

    def test_update_view_post(self):
        response = self.client.post(reverse('users:profile-edit'), {
            'bio': 'Updated Bio',
            'website': 'https://example.com',
        })
        self.profile.refresh_from_db()
        self.assertEqual(response.status_code, 302)  # Redirect to profile
        self.assertEqual(self.profile.bio, 'Updated Bio')
        self.assertEqual(self.profile.website, 'https://example.com')

    def test_update_profile_picture(self):
        with tempfile.NamedTemporaryFile(suffix=".jpg") as tmp_img:
            image = Image.new('RGB', (100, 100))
            image.save(tmp_img, format='JPEG')
            tmp_img.seek(0)

            response = self.client.post(reverse('users:profile-edit'), {
                'bio': 'Updated Bio with Picture',
                'profile_picture': tmp_img,
            })

            self.profile.refresh_from_db()
            self.assertEqual(response.status_code, 302)
            self.assertIn('profile_pics', self.profile.profile_picture.name)


class UserProfileViewTest(TestCase):
    def setUp(self):
        post_save.disconnect(create_user_profile, sender=User)
        post_save.disconnect(save_user_profile, sender=User)

        self.user = User.objects.create_user(username='testuser', password='securePassword123')
        self.profile = UserProfile.objects.create(user=self.user, bio='Initial Bio')
        self.post = Post.objects.create(title='Test Post', content='Test Content', author=self.user)
        self.client.login(username='testuser', password='securePassword123')

    def tearDown(self):
        post_save.connect(create_user_profile, sender=User)
        post_save.connect(save_user_profile, sender=User)

    def test_profile_view_get(self):
        response = self.client.get(reverse('users:user-profile', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertContains(response, 'Initial Bio')
        self.assertContains(response, 'Test Post')

    def test_profile_view_get_from_post(self):
        response = self.client.get(reverse('users:user-profile-from-post', kwargs={'post_id': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertContains(response, 'Initial Bio')
        self.assertContains(response, 'Test Post')
"""