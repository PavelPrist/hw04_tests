from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()

LEN_TEXT_STR_ = 15


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост для теста',
            group=cls.group
        )

    def test_models_post_group_have_correct_str_objects_name(self):
        """Проверяем, что у моделей Post, Group корректно работает __str__."""
        expected_obj_name = self.post.text[:LEN_TEXT_STR_]
        error_message = f"Длина вывода не 15 символов"
        self.assertEqual(expected_obj_name, self.post.__str__(), error_message)

        expected_obj_group_name = self.group.title
        self.assertEqual(expected_obj_group_name, str(self.group))

    def test_verbose_name(self):
        """verbose_name поля title совпадает с ожидаемым."""
        post = self.post
        field_verbose = {
            'text': 'Текст поста',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Группа',
        }
        for field, expected_value in field_verbose.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, expected_value)

    def test_help_text(self):
        """Help_text в полях совпадает с ожидаемым."""
        field_help_texts = {
            'text': '*Введите текст поста',
            'group': 'Группа, к которой относится пост',
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    self.post._meta.get_field(field).help_text, expected_value)
