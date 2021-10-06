from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.decorators import action

from foodgram.settings import SUB_DIR_RECIPES

User = get_user_model()


class Ingredient(models.Model):
    """Ингредиенты входящие в состав рецепта."""

    name = models.CharField(
        'Ингредиент',
        max_length=150)

    measurement_unit = models.CharField(max_length=150)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Tag(models.Model):
    """Теги рецепта."""

    name = models.TextField(
        'Название тега',
        max_length=70,
        unique=True,
        db_index=True
    )

    color = models.CharField('Цветовой HEX-код', unique=True, max_length=7)
    slug = models.SlugField('URL', unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Recipes(models.Model):
    """Рецепты блюд."""

    # REQUIRED_FIELDS = [
    #     'name',
    #     'ingredients',
    #     'tags',
    #     'author',
    #     'image',
    #     'text',
    #     'cooking_time']

    image = models.ImageField(upload_to=SUB_DIR_RECIPES)
    name = models.CharField('Название', max_length=200, )
    text = models.TextField('Описание', )

    cooking_time = models.IntegerField(
        'Время приготовления (в минутах)',
        default=1,
        validators=[
            MaxValueValidator(10000),
            MinValueValidator(1)])

    # class Rating(models.IntegerChoices):
    #     LOW = 1, _('low')
    #     MIDDLE = 2, _('midle')
    #     HIGH = 3, _('high')
    #     __empty__ = _('no rating')
    #
    # rating = models.PositiveSmallIntegerField(
    #     _('rating'),
    #     choices=Rating.choices,
    #     blank=True, null=True)

    is_favorited = models.ManyToManyField(
        'users.User',
        related_name='favorite_recipe',
        help_text='Представлен, лоигны пользователей, кто добавил этот '
                  'рецепт себе в избранное.'
    )

    is_in_shopping_cart = models.ManyToManyField(
        'users.User',
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
        'Ingredient', blank=True,
        related_name='recipes')
    # through='IngredientRecipes')

    tags = models.ManyToManyField(
        'Tag', blank=True,
        related_name='recipes')

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class TagRecipes(models.Model):
    """ В этой модели будут связаны id рецепта и id его тега."""
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tag} {self.recipe}'


class IngredientRecipes(models.Model):
    """ В этой модели будут связаны id рецепта и id его ингредиента."""
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.ingredient} {self.recipe}'




class Favorite(models.Model):
    """Избранные рецепты."""
    name = models.CharField('Название', max_length=200, )
    image = models.CharField(
        'Картинка рецепта',
        help_text='Ссылка на картинку на сайте',
        max_length=200, )
    cooking_time = models.IntegerField(
        'Время приготовления (в минутах)',
        default=1,
        validators=[MinValueValidator(1)])

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Фаворит'
        verbose_name_plural = 'Фавориты'

#
# class Follower(models.Model):
#     """Подписчики."""
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='owner')
#     subscriber = models.ForeignKey(
#         User, on_delete=models.CASCADE,
#         related_name='subscriber')
#
#     def __str__(self):
#         return f'{self.subscriber} подписан на {self.user}'
