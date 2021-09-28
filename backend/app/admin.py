from django.contrib import admin

from . import models

EVD = '-пусто-'


@admin.register(models.Ingredient)
class IntegrationAdmin(admin.ModelAdmin):
    search_fields = ('name', 'measurement_unit',)
    list_display = (
        'id',
        'name',
        'measurement_unit',
    )
    list_display_list = ('name',)
    empty_value_display = EVD


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ('name', 'color','slug',)
    list_display = (
        'id',
        'name',
        'color',
        'slug',
    )
    list_display_list = ('name',)
    empty_value_display = EVD


@admin.register(models.Recipes)
class RecipesAdmin(admin.ModelAdmin):
    search_fields = ('name', 'image','text','cooking_time',)
    list_display = ('name', 'image','text','cooking_time',)
    list_display_list = ('name',)
    empty_value_display = EVD
