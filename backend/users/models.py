from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

validate_name = RegexValidator(r'^[\w.@+-]+$')


class User(AbstractUser):
    """Модель пользователя."""

    class Roles(models.TextChoices):
        ADMIN = 'admin', _('Administrator')
        USER = 'user', _('User')

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    is_subscribed = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        related_name='subscriptions',
        help_text='На кого подисан я.'
    )

    email = models.EmailField(_('email address'), max_length=254, unique=True)
    username = models.CharField(_('username'), max_length=150, validators=[
        validate_name])
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    password = models.CharField(_('password'), max_length=150)
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

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


class Subscriptions(models.Model):
    """Кто подписался на меня."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='подписчик',
        help_text='Пользователь, который подписывается.',
        related_name='follower')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='автор',
        help_text='Пользователь, на которого подписываются.',
        related_name='following')

    def __str__(self):
        return f'{self.author}'

    class Meta:
        verbose_name = 'Подптсчик'
        verbose_name_plural = 'Подписки'
