from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import Recipe

from .models import Subscription, User

from foodgram.settings import (
    FOLLOW_ERROR_MESSAGE,
    FOLLOW_YOURSELF_ERROR_MESSAGE)


class CustomUserSerializer(UserSerializer):
    """User GET."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            )

    def get_is_subscribed(self, obj):
        """Статус подписки."""
        request = self.context.get('request')
        if request.user.is_authenticated:
            return Subscription.objects.filter(
                user=request.user, author=obj.id).exists()


class RecipeInSubscrioptionSerializer(serializers.ModelSerializer):
    """Рецепт для вывода в Subscrioption."""
    image = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscriptionPostSerializer(serializers.ModelSerializer):
    """Subscription POST."""
    queryset = User.objects.all()
    user = serializers.PrimaryKeyRelatedField(queryset=queryset)
    author = serializers.PrimaryKeyRelatedField(queryset=queryset)

    class Meta:
        model = Subscription
        fields = ('user', 'author')

    def validate(self, data):
        """Валидация  подписки."""
        if data['author'] == data['user']:
            raise serializers.ValidationError(FOLLOW_YOURSELF_ERROR_MESSAGE)
        if Subscription.objects.filter(
            author=data['author'],
            user=data['user']
        ).exists():
            raise serializers.ValidationError(FOLLOW_ERROR_MESSAGE)
        return data


class SubscriptionGetSerializer(serializers.ModelSerializer):
    """Subscription GET."""
    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')

    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
            )

    def get_is_subscribed(self, obj):
        """Статус подписки."""
        request = self.context.get('request')
        if request.user.is_authenticated:
            return Subscription.objects.filter(
                user=obj.user, author=obj.author).exists()

    def get_recipes(self, obj):
        """Рецепты на странице подписок."""
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj.author)
        if limit is not None:
            queryset = Recipe.objects.filter(
                author=obj.author
            )[:int(limit)]
        return RecipeInSubscrioptionSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        """Количество рецептов."""
        queryset = Recipe.objects.filter(author=obj.author.id).count()
        return queryset
