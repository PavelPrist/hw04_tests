from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post

User = get_user_model()

NUMBER_POSTS = 13
NUMBER_POSTS_FIRST_PAGE = 10
NUMBER_POSTS_SECOND_PAGE = 3


class PostPagesTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='NameTest')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.group2 = Group.objects.create(
            title='Тестовая группа 2',
            slug='test-slug2',
            description='Тестовое описание 2',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост для теста',
            group=cls.group
        )
        cls.template_urls = [
            (
                reverse('posts:index'),
                'posts/index.html'
            ),
            (
                reverse('posts:group_list', kwargs={'slug': cls.group.slug}),
                'posts/group_list.html'
            ),
            (
                reverse('posts:profile', kwargs={'username': cls.user}),
                'posts/profile.html'
            ),
            (
                reverse('posts:post_detail', kwargs={'post_id': cls.post.id}),
                'posts/post_detail.html'
            ),
            (
                reverse('posts:post_create'),
                'posts/create_post.html'
            ),
            (
                reverse('posts:post_edit', kwargs={'post_id': cls.post.id}),
                'posts/create_post.html'
            )
        ]

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_templates_authorised_user(self):
        """
        Тесты namespace, проверяющие, что во view-функциях используются
        правильные html-шаблоны.
        """
        for reverse_name, template in self.template_urls:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def post_response_assert(self, response):
        """Функция для тестов типы полей контекст словаря."""
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_create_post_show_correct_context(self):
        """Шаблон create_post тест типы полей в словаре context."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        self.post_response_assert(response)

    def test_post_edit_show_correct_context(self):
        """Шаблон post_edit тест типы полей в словаре context."""
        response = self.authorized_client.get(
            reverse('posts:post_edit', kwargs={'post_id': self.post.pk}))
        self.post_response_assert(response)

    def func_for_test_context(self, objects):
        """Функция для тестов верного контекста у шаблонов."""
        post_id = objects.id
        post_author = objects.author
        post_group = objects.group
        post_text = objects.text
        self.assertEqual(post_text, self.post.text)
        self.assertEqual(post_id, self.post.pk)
        self.assertEqual(post_author, self.post.author)
        self.assertEqual(post_group, self.post.group)

    def test_pages_post_detail_show_correct_context(self):
        """Шаблон post_detail сформирован с верным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.pk})
        )
        objects = response.context.get('post')
        self.func_for_test_context(objects)

    def test_post_with_group_on_pages_show_correct_context(self):
        """
        Тест - пост, добавленный в группу, выводится корректно на страницы.
        """
        reverse_objects = [
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': self.group.slug}),
            reverse('posts:profile', kwargs={'username': self.user}),
        ]
        for reverse_name in reverse_objects:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                objects = response.context['page_obj'][0]
                self.func_for_test_context(objects)

    def test_post_not_in_over_group(self):
        """Тест НЕ_нахождения поста в чужой группе."""
        reverse_name_group2 = reverse(
            'posts:group_list', kwargs={'slug': self.group2.slug})
        response = self.authorized_client.get(reverse_name_group2)
        self.assertNotContains(response, self.post)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='NameTest')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.posts = Post.objects.bulk_create(
            [
                Post(
                    text=f'Тестовые посты номер {n}',
                    author=cls.user,
                    group=cls.group
                )
                for n in range(NUMBER_POSTS)
            ]
        )

    def setUp(self):
        self.guest_client = Client()

    def pagination_test_setup(self, url_params, expected_count):
        """Функция для тестирования шаблонов с пагинацией."""
        reverse_pages_names = [
            reverse('posts:index') + url_params,
            reverse(
                'posts:group_list',
                kwargs={'slug': self.group.slug}) + url_params,
            reverse(
                'posts:profile',
                kwargs={'username': self.user}) + url_params,
        ]
        for reverse_name in reverse_pages_names:
            with self.subTest(reverse_name=reverse_name):
                response = self.client.get(reverse_name)
                self.assertEqual(
                    len(response.context['page_obj']), expected_count
                )

    def test_first_page_contains_ten_records(self):
        """Проверка: количество постов на первой странице равно 10."""
        self.pagination_test_setup('', NUMBER_POSTS_FIRST_PAGE)

    def test_second_page_contains_three_records(self):
        """Проверка: на второй странице должно быть три поста."""
        self.pagination_test_setup('?page=2', NUMBER_POSTS_SECOND_PAGE)
