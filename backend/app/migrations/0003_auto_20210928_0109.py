# Generated by Django 3.0.5 on 2021-09-27 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210928_0056'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipes',
            name='ingredients',
        ),
        migrations.AddField(
            model_name='recipes',
            name='ingredients',
            field=models.ManyToManyField(to='app.Ingredient', verbose_name='ingredient'),
        ),
    ]