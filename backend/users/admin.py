from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import User

EVD = '-пусто-'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name',
                    'is_staff', 'phone', 'is_subscribed')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email',
                                         'phone', 'is_subscribed')}),
        (_('subscriptions'), {'fields': ('subscriptions',)}),

        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups',
                       'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )



    # search_fields = ('username', 'email',)
    # list_display = (
    #     'id',
    #     'username',
    #     'email',
    #     'first_name',
    #     'last_name',
    #     'password'
    # )
    # list_display_list = ('email',)
    # empty_value_display = EVD