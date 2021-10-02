from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

from foodgram.settings import SUB_DIR_RECIPES

User = get_user_model()


class Ingredient(models.Model):
    """Ингредиенты."""
    # REQUIRED_FIELDS = ['name', 'measurement_unit']

    name = models.CharField(
        'Ингредиент',
        # db_index=True,
        max_length=150)
    measurement_unit = models.CharField(max_length=150)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Tag(models.Model):
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
    REQUIRED_FIELDS = ['name', 'ingredients', 'tags', 'author', 'image',
                       'text',
                       'cooking_time']
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='автор',
        null=True,
        help_text='Пользователь составивший рецепт.',
        related_name='recipes')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='IngredientOfRecipes')
    tags = models.ManyToManyField('Tag', related_name='recipes', )
    image = models.ImageField(upload_to=SUB_DIR_RECIPES)
    name = models.CharField('Название', max_length=200, )
    text = models.TextField('Описание', )
    cooking_time = models.IntegerField('Время приготовления (в минутах)',
                                       default=1,
                                       validators=[
                                           MaxValueValidator(10000),
                                           MinValueValidator(1)
                                       ])
    is_favorited = models.BooleanField('Фаворит', default=True,
                                       help_text='Показывать только рецепты, '
                                                 'находящиеся в списке '
                                                 'избранного.')
    is_in_shopping_cart = models.BooleanField('Покупка', default=True,
                                              help_text='Показывать только '
                                                        'рецепты, находящиеся '
                                                        'в списке покупок.')

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class IngredientOfRecipes(models.Model):
    """Описание ингредиента для рецепта."""
    ingredient = models.ForeignKey(Ingredient, verbose_name='Ингредиент',
                                   on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    # amount = models.IntegerField(verbose_name='Количество')

    def __str__(self):
        return f'{self.ingredient} {self.recipe}'

# class Subscription(models.Model):
#     following = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         verbose_name='автор',
#         help_text='Пользователь, на которого подписываются.',
#         related_name='follow')
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         verbose_name='подписчик',
#         help_text='Кто подписался (Подписчик)',
#         related_name='follower')
#
#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['user', 'following'],
#                 name='unique user_following',
#             )
#         ]


class Favorite(models.Model):
    """Избранные рецепты."""
    name = models.CharField('Название', max_length=200, )
    image = models.CharField('Картинка рецепта',
                             help_text='Ссылка на картинку на сайте',
                             max_length=200, )
    cooking_time = models.IntegerField('Время приготовления (в минутах)',
                                       default=1,
                                       validators=[MinValueValidator(1)])

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Фаворит'
        verbose_name_plural = 'Фавориты'


class Follower(models.Model):
    """Подписчики."""
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='owner')
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='subscriber')

    def __str__(self):
        return f'{self.subscriber} подписан на {self.user}'
