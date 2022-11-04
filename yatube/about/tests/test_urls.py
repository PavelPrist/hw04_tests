from http import HTTPStatus

from django.test import Client, TestCase


class AboutUrlsTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.guest_client = Client()

        cls.urls_template = {
            '/about/author/': 'about/author.html',
            '/about/tech/': 'about/tech.html',
            '/about/jeday/': 'about/jeday.html'
        }

    def test_urls_app_about_exist_desired_location(self):
        """Test that urls of app about are availability."""
        for urls in self.urls_template:
            with self.subTest(urls=urls):
                response = self.guest_client.get(urls)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_uses_correct_templates(self):
        """Test that urls have correct templates."""
        for urls, templates in self.urls_template.items():
            with self.subTest(urls=urls):
                response = self.guest_client.get(urls)
                self.assertTemplateUsed(response, templates)
