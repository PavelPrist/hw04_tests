from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class UsersUrlTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.template_url_names = {
            '/auth/login/': 'users/login.html',
            '/auth/signup/': 'users/signup.html',
            '/auth/password_reset_form/': 'users/password_reset_form.html',
            '/auth/password_reset/done/': 'users/password_reset_done.html',
            '/auth/reset/<uidb64>/<token>/':
                'users/password_reset_confirm.html',
            '/auth/reset/done/': 'users/password_reset_complete.html',
            '/auth/password_change/': 'users/password_change_form.html',
            '/auth/password_change/done/': 'users/password_change_done.html',
            '/auth/contact/': 'users/contact.html',
            '/auth/logout/': 'users/logged_out.html',
        }

    def setUp(self):
        self.user_auth = User.objects.create_user(username='AuthUser')
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user_auth)

    def test_urls_app_users_exist_desired_location(self):
        """Test that urls of app users are availability."""
        for urls in self.template_url_names:
            with self.subTest(urls=urls):
                response = self.authorized_client.get(urls)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_response_not_auth(self):
        """Test that not auth user get response status 302"""
        url_status = {
            reverse('users:password_change'): HTTPStatus.FOUND,
            reverse('users:password_change_done'): HTTPStatus.FOUND
        }
        for reverse_url, status_code in url_status.items():
            with self.subTest(reverse_url=reverse_url):
                response = self.guest_client.get(reverse_url)
                self.assertEqual(response.status_code, status_code)

    def test_urls_response_guest_user_redirected(self):
        """Test that guest user redirected to correct pages."""
        url_status = {
            reverse('users:password_change'):
                reverse('users:login') + '?next='
                + reverse('users:password_change'),
            reverse('users:password_change_done'):
                reverse('users:login') + '?next='
                + reverse('users:password_change_done')
        }
        for url_reverse, redirect_url in url_status.items():
            with self.subTest(url_reverse=url_reverse):
                response = self.guest_client.get(url_reverse)
                self.assertRedirects(response, redirect_url)

    def test_urls_uses_correct_templates(self):
        """Test that urls have correct templates."""
        for urls, templates in self.template_url_names.items():
            with self.subTest(urls=urls):
                response = self.authorized_client.get(urls)
                self.assertTemplateUsed(response, templates)


class LoginTestCase(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user('Pavel',
                                             'supernio@yandex.ru',
                                             'PavelPavel')

    def testLogin(self):
        self.guest_client.login(username='Pavel', password='PavelPavel')
        response = self.guest_client.get(reverse('users:password_change'))
        self.assertEqual(response.status_code, 200)
