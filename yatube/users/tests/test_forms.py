from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms

User = get_user_model()


class UsersFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        self.guest_client = Client()

    def test_signup_form_new_user_is_corect(self):
        """Test that form in signup is working correctly."""
        users_count = User.objects.count()
        form_data = {
            'first_name': 'Pavel',
            'last_name': 'Ser',
            'username': 'Pav',
            'email': 'supernio@yandex.ru',
            'password1': '!passWoR12D',
            'password2': '!passWoR12D'
        }
        response = self.guest_client.post(
            reverse('users:signup'),
            data=form_data,
            follow=True
        )
        user_last = User.objects.latest('id')
        self.assertRedirects(response, reverse('posts:index'))
        self.assertEqual(User.objects.count(), users_count + 1)
        self.assertEqual(user_last.username, form_data['username'])
        self.assertEqual(user_last.first_name, form_data['first_name'])
        self.assertEqual(user_last.last_name, form_data['last_name'])