from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from django.utils.translation import activate


class TestViews(TestCase):
    def test_home_view(self):
        activate('en')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/home.html')

    def test_about_view(self):
        activate('en')
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/about.html')

    def test_contact_view_get(self):
        activate('en')
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/contact.html')

    def test_contact_view_post_invalid_captcha(self):
        response = self.client.post(reverse('contact'), {
            'name': 'Test User',
            'email': 'test@example.com',
            'message': 'This is a test message.',
            'captcha': '7'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/contact.html')

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Incorrect captcha. Please try again.")

    def test_contact_view_post_valid_captcha(self):
        response = self.client.post(reverse('contact'), {
            'name': 'Test User',
            'email': 'test@example.com',
            'message': 'This is a test message.',
            'captcha': '8'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/contact.html')

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Your message has been sent successfully!")