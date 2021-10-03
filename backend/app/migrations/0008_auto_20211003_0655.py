# Generated by Django 3.0.5 on 2021-10-03 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20211003_0654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipes',
            name='is_favorited',
            field=models.IntegerField(choices=[(0, 1), (1, 0)], default=0, help_text='Показывать только рецепты, находящиеся в списке избранного.', verbose_name='Фаворит'),
        ),
        migrations.AlterField(
            model_name='recipes',
            name='is_in_shopping_cart',
            field=models.IntegerField(choices=[(0, 1), (1, 0)], default=0, help_text='Показывать только рецепты, находящиеся в списке покупок.', verbose_name='Покупка'),
        ),
    ]
