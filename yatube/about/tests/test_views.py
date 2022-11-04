from django.test import Client, TestCase
from django.urls import reverse


class AboutPagesTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.guest_client = Client()

        cls.names_template = {
            reverse('about:author'): 'about/author.html',
            reverse('about:tech'): 'about/tech.html',
            reverse('about:jeday'): 'about/jeday.html'
        }

    def test_views_uses_correct_templates(self):
        """Test namespaces-views uses correct templates."""
        for names, templates in self.names_template.items():
            with self.subTest(names=names):
                response = self.guest_client.get(names)
                self.assertTemplateUsed(response, templates)

