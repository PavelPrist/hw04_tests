from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')
        labels = {
            'group': 'Группа для Вашего поста',
        }
        help_texts = {
            'group': 'выберите группу из списка или оставьте пустым',
        }
