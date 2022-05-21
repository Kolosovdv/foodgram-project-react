from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _


class User(AbstractUser):
    """Кастомная модель юзера."""
    
    email = models.EmailField(
        _('email address'),
        unique=True,
    )   
    #is_subscribed = models.BooleanField() № при запросе http://localhost/api/users/{id} возвращает булен, что Подписан ли текущий пользователь на этого 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.email}, {self.username}'
        

class Subscription (models.Model): #написать вьюсет для обработки
    #текущий пользователь
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    #автор, на которого подписан текущий пользователь
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        ordering = ['user']
# Create your models here.
