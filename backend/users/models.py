from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

validate_name = RegexValidator('^[\w.@+-]+$')


class User(AbstractUser):
    """Модель пользователя."""

    class Roles(models.TextChoices):
        ADMIN = 'admin', _('Administrator')
        USER = 'user', _('User')

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']


    email = models.EmailField(_('email address'), max_length=254, unique=True)
    username = models.CharField(max_length=150, validators=[validate_name])
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    role = models.CharField(
        _('role'), choices=Roles.choices, default=Roles.USER, max_length=30
    )

    @property
    def is_authenticated(self):
        """Был ли пользователь аутентифицирован. Всегда True."""
        return True

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser


    @property
    def is_user(self):
        return self.role == 'user'

    def __str__(self):
        return self.email
