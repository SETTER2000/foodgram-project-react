from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

from foodgram.settings import SUB_DIR_RECIPES

User = get_user_model()


class Ingredient(models.Model):
    """Ингредиенты."""
    REQUIRED_FIELDS = ['name', 'measurement_unit']

    name = models.CharField(
        "Ингредиент",
        db_index=True,
        max_length=150)
    measurement_unit = models.CharField(max_length=150)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"


class Tag(models.Model):
    name = models.TextField(
        "Название тега",
        max_length=70,
        unique=True,
        db_index=True
    )
    color = models.CharField('Цветовой HEX-код', unique=True, max_length=7)
    slug = models.SlugField("URL", unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Recipes(models.Model):
    """Рецепты блюд."""
    REQUIRED_FIELDS = ['name', 'ingredients', 'tags','author', 'image', 'text',
                       'cooking_time']
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='автор',
        null=True,
        help_text='Пользователь составивший рецепт.',
        related_name='author_recipes')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='IngredientOfRecipes')
    tags = models.ManyToManyField(Tag, verbose_name='Список тегов.', )
    image = models.ImageField(upload_to=SUB_DIR_RECIPES)
    name = models.CharField("Название", max_length=200, )
    text = models.TextField("Описание", )
    cooking_time = models.IntegerField('Время приготовления (в минутах)',
                                       default=1,
                                       validators=[
                                           MaxValueValidator(10000),
                                           MinValueValidator(1)
                                       ])

    # def __str__(self) -> str:
    #     return self.name

    class Meta:
        ordering = ("name",)
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"


class IngredientOfRecipes(models.Model):
    """Описание ингредиента для рецепта."""
    ingredient = models.ForeignKey('Ingredient', verbose_name='Ингредиент',
                                   on_delete=models.CASCADE)
    recipe = models.ForeignKey('Recipes', on_delete=models.CASCADE)
    amount = models.IntegerField(verbose_name='Количество')
