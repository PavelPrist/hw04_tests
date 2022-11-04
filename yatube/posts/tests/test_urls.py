from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from ..models import Group, Post

User = get_user_model()


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_homepage(self):
        """Проверка доступности главной страницы всем пользователям."""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, HTTPStatus.OK)


class PostUrlTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user_auth = User.objects.create_user(username='NameAuth')
        cls.user = User.objects.create_user(username='NameTest')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост для теста',
            group=cls.group
        )
        cls.template_url_names = {
            "/": "posts/index.html",
            f"/group/{cls.group.slug}/": "posts/group_list.html",
            f"/profile/{cls.user.username}/": "posts/profile.html",
            f"/posts/{cls.post.id}/": "posts/post_detail.html",
            f"/posts/{cls.post.id}/edit/": "posts/create_post.html",
            "/create/": "posts/create_post.html",
        }
        cls.template_url = [
            "/",
            f"/group/{cls.group.slug}/",
            f"/profile/{cls.user}/",
            f"/posts/{cls.post.id}/",
        ]

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.authorized_user_not_author = Client()
        self.authorized_user_not_author.force_login(self.user_auth)

    def test_unexisting_page_return_notfound(self):
        """Тест возврата ошибки с несуществующей страницы."""
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_posts_url_available_non_authorised(self):
        """Проверка доступности страниц неавторизованному пользователю."""
        for address in self.template_url:
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_posts_url_available_authorised(self):
        """Проверка доступности страниц авторизованному пользователю."""
        for address in self.template_url_names:
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_posts_url_authorized_users_uses_correct_template(self):
        """
        Проверка соответствия шаблонов запросу
        авторизованного пользователя.
        """
        for address, template in self.template_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_posts_url_redirect_for_non_authorized_users(self):
        """Проверка для анонимного пользователя
        редиректа на страницу логина со страниц post_edit, post_create."""

        template_url_names = {
            '/create/': '/auth/login/?next=/create/',
            f'/posts/{self.post.id}/edit/': '/auth/login/?next=/posts/1/edit/',
        }

        for address, urls in template_url_names.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address, follow=True)
                self.assertRedirects(response, urls)

    def test_posts_url_redirect_for_authorized_users_auth(self):
        """Проверка для авторизованного пользователя
        не автора поста редиректа с post_edit на сам пост."""

        address = f'/posts/{self.post.id}/edit/'
        template = f'/posts/{self.post.id}/'
        response = self.authorized_user_not_author.get(address, follow=True)
        self.assertRedirects(response, template)
