from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


validate_name = RegexValidator(r'^[\w.@+-]+$')

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        user = self.create_user(
            username, email, password=password, **extra_fields
        )
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name="Электронная почта",
        help_text="Введите электронную почту",
    )
    username = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Имя пользователя",
        help_text="Введите имя пользователя",
    )
    first_name = models.CharField(
        max_length=255,
        verbose_name="Имя",
        help_text="Введите имя пользователя",
    )
    last_name = models.CharField(
        max_length=255,
        verbose_name="Фамилия",
        help_text="Введите фамилию пользователя",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Статус активности",
        help_text="Блокировка пользователя",
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name="Статус администратора",
        help_text="Укажите статус пользователя",
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name="Статус суперпользователя",
        help_text="Указывает, есть ли у пользователя суперправа",
    )
    date_joined = models.DateTimeField(
        default=timezone.now,
        verbose_name="Дата регистрации",
        help_text="Дата регистрации пользователя",
    )
    last_login = models.DateTimeField(
        null=True,
        verbose_name="Последнее посещение",
        help_text="Последнее посещение пользователя",
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username", "first_name", "last_name")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def get_full_name(self):
        return f"{self.first_name} - {self.last_name}"

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

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
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписки'
