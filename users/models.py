from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Модель пользователя с некоторыми настраиваемыми полями."""

    class Roles(models.TextChoices):
        ADMIN = 'admin', _('Administrator')
        MODER = 'moderator', _('Moderator')
        USER = 'user', _('User')

    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(
        _('role'), choices=Roles.choices, default=Roles.USER, max_length=30
    )
    confirmation_code = models.CharField(
        _('confirmation code'), max_length=100, blank=True
    )

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    @property
    def is_moder(self):
        return self.role == 'moderator' or self.is_staff

    @property
    def is_user(self):
        return self.role == 'user'

    class Meta:
        ordering = ('username',)
