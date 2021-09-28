from django.contrib import admin

from . import models

EVD = '-пусто-'


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ('username', 'email',)
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'password'
    )
    list_display_list = ('email',)
    empty_value_display = EVD
