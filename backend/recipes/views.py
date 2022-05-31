from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from logic.filters import IngredientFilter, RecipeFilter
from logic.paginations import CustomPageNumberPaginator
from logic.permissions import AuthorOrAdminOrRead
from recipes.models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                            ShoppingList, Tag)

from .serializers import (IngredientSerializer, RecipeInFollowSerializer,
                          RecipeSerializer, TagSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny, )
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny, )
    filter_backends = [DjangoFilterBackend]
    filter_class = IngredientFilter
    search_fields = ('^name',)
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (AuthorOrAdminOrRead, )
    filter_backends = [DjangoFilterBackend, ]
    filter_class = RecipeFilter
    pagination_class = CustomPageNumberPaginator

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
            methods=['post', 'delete'],
            detail=True,
            permission_classes=[IsAuthenticated]
            )
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            recipe = get_object_or_404(Recipe, pk=pk)
            Favorite.objects.create(user=request.user, recipe=recipe)
            serializer = RecipeInFollowSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        favorite = Favorite.objects.filter(user=request.user, recipe=pk)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
            methods=['post', 'delete'],
            detail=True,
            permission_classes=[IsAuthenticated]
            )
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            recipe = get_object_or_404(Recipe, pk=pk)
            ShoppingList.objects.create(user=request.user, recipe=recipe)
            serializer = RecipeInFollowSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        favorite = ShoppingList.objects.filter(user=request.user, recipe=pk)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[AuthorOrAdminOrRead]
        )
    def download_shopping_cart(self, request):
        ingredients = IngredientInRecipe.objects.filter(
            recipe__shopping_list__user=request.user).values_list(
            'ingredient__name', 'ingredient__measurement_unit').order_by(
                'ingredient__name').annotate(ingredient_total=Sum('amount'))
        text = 'Список покупок: \n'
        shoplist = {}
        # for ingredients in ingredients:
        #     name, measurement_unit, amount = ingredients
        #     if name not in shoplist:
        #         shoplist[name] = {
        #             'единица измерения': measurement_unit,
        #             'количество': amount
        #         }
        #     else:
        #         shoplist[name]['amount'] += amount
        for ingredients in ingredients:
            name, measurement_unit, amount = ingredients
            # shoplist[name] = {
            #         'единица измерения': measurement_unit,
            #         'количество': amount
            #     }
            text += f'({name} = {amount} {measurement_unit}\n)'    
        #text += f'{str(shoplist)}'
        response = HttpResponse(text, 'Content-Type: text/plane')
        response['Content-Disposition'] = 'attachment; filename="shoplist.txt"'
        return response
  