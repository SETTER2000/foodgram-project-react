from django.contrib import admin

from backend.foodgram.settings import EVD

from . import models


@admin.register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ('name', 'measurement_unit',)
    list_display = ('id', 'name', 'measurement_unit',)
    list_display_list = ('name',)
    empty_value_display = EVD


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ('name', 'color', 'slug',)
    list_display = ('id', 'name', 'color', 'slug',)
    list_display_list = ('name',)
    empty_value_display = EVD


@admin.register(models.Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    search_fields = ('name', 'image', 'cooking_time',)
    list_display = ('id', 'name', 'image', 'cooking_time',)
    list_display_list = ('name',)
    empty_value_display = EVD


@admin.register(models.Recipes)
class RecipesAdmin(admin.ModelAdmin):
    search_fields = ('id', 'name', 'image', 'text', 'author', 'cooking_time',)
    list_display = ('id', 'name', 'image', 'text', 'author', 'cooking_time',)
    list_display_list = ('name',)
    empty_value_display = EVD


@admin.register(models.RecipesIngredients)
class RecipesIngredientsAdmin(admin.ModelAdmin):
    search_fields = ('id', 'ingredient', 'recipe', 'amount')
    list_display = ('id', 'ingredient', 'recipe', 'amount')
    list_display_list = ('id',)
    empty_value_display = EVD
