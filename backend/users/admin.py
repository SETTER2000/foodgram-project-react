from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import User, Subscriptions

EVD = '-пусто-'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('id','username', 'email', 'first_name', 'last_name',
                    'is_staff')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('is_subscribed'), {'fields': ('is_subscribed',)}),

        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups',
                       'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

#
# @admin.register(Subscriptions)
# class SubscriptionsAdmin(admin.ModelAdmin):
#     search_fields = (
#         'id', 'name','user', 'author')
#     list_display = (
#          'id','user',  'author')
#     list_display_list = ('name',)
#     empty_value_display = EVD
