from django.db import models

from posts.validators import validate_not_empty


class Contact(models.Model):

    name = models.CharField(
        'Представьтесь, пожалуйста',
        max_length=100,
        validators=[validate_not_empty],
        help_text='*Введите свое имя'
    )
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    body = models.TextField()
    is_answered = models.BooleanField(default=False)
