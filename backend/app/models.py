from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Ingredient(models.Model):
    """Ингредиенты."""
    REQUIRED_FIELDS = ['name', 'measurement_unit']
    name = models.CharField(
        "Ингрелиент",
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
        db_index=True,
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

    ingredients = models.ManyToManyField(Ingredient,verbose_name="ingredient")
    tags = models.ManyToManyField(Tag, verbose_name='Список тегов.', )
    image = models.ImageField(
        'Картинка',
        upload_to='recipes',
        blank=True
    )
    name = models.CharField("Название", max_length=200, )
    text = models.TextField("Описание", )
    cooking_time = models.IntegerField('Время приготовления (в минутах)',
                                       default=1,
                                       validators=[
                                           MaxValueValidator(10000),
                                           MinValueValidator(1)
                                       ])

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
