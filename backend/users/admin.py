from django.contrib import admin

from backend.users.models import User

EVD = '-пусто-'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # search_fields = ('username', 'email',)
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'password',
        'role',
    )
    list_display_links = ('username', 'email')
    list_editable = ('role',)
    list_filter = ('role',)
    empty_value_display = EVD
