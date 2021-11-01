from app.models import Favorite, Ingredient, Recipes, RecipesIngredients, Tag
from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html
from utilites.mixins import AdminColor


@admin.register(Tag)
class TagAdmin(AdminColor, admin.ModelAdmin):
    list_display = ("name", "slug", "colored_circle")
    prepopulated_fields = {
        "slug": ("name",),
    }
    ordering = ("id",)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ('name', 'measurement_unit',)
    list_display = ('id', 'name', 'measurement_unit',)
    list_display_list = ('name',)
    empty_value_display = settings.EVD


# @admin.register(Tag)
# class TagAdmin(admin.ModelAdmin):
#     search_fields = ('name', 'color', 'slug',)
#     list_display = ('id', 'name', 'color', 'slug',)
#     list_display_list = ('name',)
#     empty_value_display = settings.EVD


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    search_fields = ('name', 'image', 'cooking_time',)
    list_display = ('id', 'name', 'image', 'cooking_time',)
    list_display_list = ('name',)
    empty_value_display = settings.EVD


@admin.register(RecipesIngredients)
class RecipesIngredientsAdmin(admin.ModelAdmin):
    list_display = ("id", "recipe", "ingredient")
    search_fields = ("recipe__name",)


class IngridientItemAdmin(admin.StackedInline):
    model = Recipes.ingredients.through
    extra = 0


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    inlines = (IngridientItemAdmin,)
    list_display = (
        "id",
        "author",
        "name",
        "cooking_time",
        "image_list_preview",
    )
    exclude = ("ingredients",)
    search_fields = ("name", "author__username", "author__email")
    list_filter = ("tags",)
    filter_horizontal = ("tags",)

    readonly_fields = ("image_change_preview",)

    def image_change_preview(self, obj):
        if obj.image:
            url = obj.image.url
            return format_html(
                '<img src="{}" width="600" height="300" style="'
                "border: 2px solid grey;"
                'border-radius:50px;" />'.format(url)
            )
        return "Превью"

    image_change_preview.short_description = "Превью"

    def image_list_preview(self, obj):
        if obj.image:
            url = obj.image.url
            return format_html(
                '<img src="{}" width="100" height="50" style="'
                "border: 1px solid grey;"
                'border-radius:10px;" />'.format(url)
            )
        return "Картинка"

    image_list_preview.short_description = "Картинка"
