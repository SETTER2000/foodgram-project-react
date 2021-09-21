from django.contrib import admin

from users.models import User

EVD = '-пусто-'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'role',
        'first_name',
        'last_name',
    )
    search_fields = ('username', 'email')
    empty_value_display = EVD
