from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

# def validate_name(value):
#     if not re.compile(r'^[\w.@+-]+\z').match(value):
#         raise ValidationError('Enter Number Correctly')


validate_name = RegexValidator('^[\w.@+-]+$')


class User(AbstractUser):
    """Модель пользователя с некоторыми настраиваемыми полями."""
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    class Roles(models.TextChoices):
        ADMIN = 'admin', _('Administrator')
        MODER = 'moderator', _('Moderator')
        USER = 'user', _('User')

    email = models.EmailField(
        _('email address'),
        max_length=254
    )
    password = models.CharField(
        _('password'),
        max_length=150
    )
    last_name = models.CharField(
        _('last name'),
        max_length=150,
        validators=[validate_name]
    )
    first_name = models.CharField(
        _('name'),
        max_length=150
    )
    username = models.CharField(
        _('username'),
        unique=True,
        max_length=150,
        validators=[validate_name]
    )
    role = models.CharField(
        _('role'),
        choices=Roles.choices,
        default=Roles.USER,
        max_length=30
    )
    confirmation_code = models.CharField(
        _('confirmation code'),
        max_length=100,
        blank=True
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
