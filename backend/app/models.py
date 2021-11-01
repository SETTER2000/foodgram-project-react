from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import TextField
from django.utils.translation import gettext_lazy as _
from rest_framework.fields import CharField
from utilites.utils import slugify
from app.configuration.settings import prod
DJANGO_SETTINGS_MODULE=prod

User = get_user_model()


class Ingredient(models.Model):
    """Ингредиенты входящие в состав рецепта."""
    name = models.CharField(
        'Ингредиент',
        max_length=150)

    measurement_unit = models.CharField(max_length=150)

    def __str__(self) -> CharField:
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Tag(models.Model):
    """Теги рецепта."""

    class Color(models.TextChoices):
        ORANGE = '#E26C2D', _('Оранжевый')
        GREEN = '#49B64E', _('Зелёный')
        PURPLE = '#8775D2', _('Фиолетовый')

    name = models.TextField(
        'Название тега',
        max_length=70,
        unique=True,
        db_index=True
    )
    color = models.CharField(
        'Цвет тега',
        unique=True,
        max_length=7,
        choices=Color.choices,
        help_text='Выберите цвет из списка',
    )
    slug = models.SlugField(
        'URL',
        unique=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> TextField:
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Recipes(models.Model):
    """Рецепты блюд."""
    REQUIRED_FIELDS = [
        'name',
        'ingredients',
        'tags',
        'image',
        'text',
        'cooking_time']

    image = models.ImageField(upload_to=settings.SUB_DIR_RECIPES)
    name = models.CharField(
        'Название',
        max_length=200, )
    text = models.TextField('Описание', )

    cooking_time = models.IntegerField(
        'Время приготовления (в минутах)',
        default=1,
        validators=[
            MaxValueValidator(
                1000,
                message='Время приготовления макс. 1000 мин.'),
            MinValueValidator(
                1,
                message='Время приготовления нужно заполнить.')])

    is_favorited = models.ManyToManyField(
        'users.User',
        blank=True,
        related_name='favorite_recipe',
        help_text='Представлен, лоигны пользователей, кто добавил этот '
                  'рецепт себе в избранное.')

    is_in_shopping_cart = models.ManyToManyField(
        'users.User',
        blank=True,
        related_name='shopping_recipe',
        help_text='Показывать только рецепты, находящиеся в списке покупок.')

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='автор',
        null=True,
        help_text='Пользователь составивший рецепт.',
        related_name='recipes')

    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipesIngredients',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Ингредиенты',
        help_text='Выберите ингредиенты из списка',
    )

    tags = models.ManyToManyField(
        'Tag',
        blank=True,
        related_name='recipes')

    def __str__(self) -> CharField:
        return self.name

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class RecipesIngredients(models.Model):
    """ В этой модели будут связаны id рецепта и
    id его ингредиента."""
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipes,
        verbose_name='Рецепт',
        on_delete=models.CASCADE)
    amount = models.IntegerField(
        _('Количество'),
        default=1,
        validators=[
            MinValueValidator(1, message='Количество нужно заполнить.')])

    class Meta:
        unique_together = (
            'ingredient',
            'recipe',
            'amount')


class RecipesTags(models.Model):
    """ В этой модели будут связаны id рецепта и id его тега."""
    tag = models.ForeignKey(
        Tag,
        verbose_name='Тег',
        on_delete=models.CASCADE)
    recipes = models.ForeignKey(
        Recipes,
        verbose_name='Рецепт',
        on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tag} {self.recipes}'


class Favorite(models.Model):
    """Избранные рецепты."""
    name = models.CharField(
        'Название',
        max_length=200, )
    image = models.CharField(
        'Картинка рецепта',
        help_text='Ссылка на картинку на сайте',
        max_length=200, )
    cooking_time = models.IntegerField(
        'Время приготовления (в минутах)',
        default=1,
        validators=[
            MinValueValidator(
                1,
                message='Время приготовления нужно заполнить.')])

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Фаворит'
        verbose_name_plural = 'Фавориты'
