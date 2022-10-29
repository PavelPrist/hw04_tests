from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post, User

User = get_user_model()


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='NameTest')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание группы',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост для теста',
            group=cls.group
        )

    def setUp(self):
        self.guest_user_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def asserts_func_for_tests(self, response, form_data):
        """Функция для тестов assert."""
        post_last = Post.objects.latest('id')
        self.assertEqual(post_last.text, form_data['text'])
        self.assertEqual(post_last.author, self.user)
        self.assertEqual(post_last.group_id, form_data['group'])
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_post_form_valid_by_authorized_user(self):
        """
        Тест: валидная форма create_post,
        авторизованный пользователь создает запись в базе данных.
        """
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовая запись',
            'group': self.group.id
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse('posts:profile', kwargs={'username': self.user.username})
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(Post.objects.filter(text=form_data['text']).exists())
        self.asserts_func_for_tests(response, form_data)

    def test_post_edit_form_valid_by_authorized_user(self):
        """
        Тест: валидная форма edite_post,
        авторизованный пользователь меняет запись в базе данных.
        """
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Отредактированный текст',
            'group': self.group.id
        }
        response = self.authorized_client.post(
            reverse(
                'posts:post_edit',
                args=[self.post.id]),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse('posts:post_detail', kwargs={'post_id': self.post.id})
        )
        self.assertEqual(Post.objects.count(), posts_count)
        self.asserts_func_for_tests(response, form_data)

    def test_post_create_redirect_with_none_authorized(self):
        """
        Тест post_create для неавторизованного: Валидная форма перенаправляет
        на страницу авторизации.
        """
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст',
            'group': self.group.id
        }
        response = self.guest_user_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Post.objects.count(), posts_count)
        redirect = '/auth/login/?next=/create/'
        self.assertRedirects(response,redirect)


