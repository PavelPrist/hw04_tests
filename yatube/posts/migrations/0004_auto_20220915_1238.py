# Generated by Django 2.2.9 on 2022-09-15 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20220914_1415'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='slug_url',
            new_name='slug',
        ),
        migrations.AlterField(
            model_name='group',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Заголовок'),
        ),
    ]
