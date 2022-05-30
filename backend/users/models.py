from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _


class User(AbstractUser):
    """Кастомная модель юзера."""
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')
    #REQUIRED_FIELDS = ['username']
    username = models.CharField(
        verbose_name='Логин',
        max_length=150,
        null=False,
        unique=True
    )
    email = models.EmailField(
        max_length=254,
        blank=True,
        unique=True,
        null=False,
        verbose_name='Адрес электронной почты'
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Фамилия'
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'


class Subscription (models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        ordering = ('user',)

    def __str__(self):
        return f'{self.author}, {self.user}'