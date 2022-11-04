from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms

User = get_user_model()


class UsersPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.template_url_names = {
            reverse('users:login'): 'users/login.html',
            reverse('users:signup'): 'users/signup.html',
            reverse('users:password_reset_form'): 'users/password_reset_form.html',
            reverse('users:password_reset_done'): 'users/password_reset_done.html',
            reverse(
                'users:password_reset_confirm',
                kwargs={'uidb64': 'NA', 'token': 'x'}):
                'users/password_reset_confirm.html',
            reverse('users:password_reset_complete'): 'users/password_reset_complete.html',
            reverse('users:password_change'): 'users/password_change_form.html',
            reverse('users:password_change_done'): 'users/password_change_done.html',
            reverse('users:contact'): 'users/contact.html',
            reverse('users:logout'): 'users/logged_out.html',
        }

    def setUp(self):
        self.user_auth = User.objects.create_user(username='AuthUser')
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user_auth)

    def test_namespace_views_uses_correct_templates(self):
        """Test that namespace-views have correct templates."""
        for name, templates in self.template_url_names.items():
            with self.subTest(name=name):
                response = self.authorized_client.get(name)
                self.assertTemplateUsed(response, templates)

    def test_signup_page_has_correct_context(self):
        """Template signup has correct context."""
        response = self.authorized_client.get(reverse('users:signup'))
        form_fields = {
            'first_name': forms.fields.CharField,
            'last_name': forms.fields.CharField,
            'username': forms.fields.CharField,
            'email': forms.fields.EmailField
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)
