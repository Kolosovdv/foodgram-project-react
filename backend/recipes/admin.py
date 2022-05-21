from django.contrib import admin

from recipes.models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                            ShoppingList, Tag)


class IngredientInRecipeInline(admin.TabularInline):
    model = IngredientInRecipe


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'color',
        'slug',
    )
    list_filter = ('name',)
    search_fields = ('name',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit',
    )
    list_filter = ('name',)
    search_fields = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    # Перечисляем поля, которые должны отображаться в админке
    inlines = (
        IngredientInRecipeInline,
    )
    
    list_display = ('id','name', 'author', 'text', 'cooking_time', 'image') 
    # Добавляем интерфейс для поиска по тексту постов
    search_fields = ('name',)
    list_filter = ('author', 'name', 'tags')
    exclude = ('ingredients',)
    
    # @staticmethod
    # def favorite_count(obj):
    #     return Favorite.objects.filter(recipe=obj).count()


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'user',)
    search_fields = ('user', 'recipe',)


class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe',)
    search_fields = ('user', 'recipe',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingList, ShoppingListAdmin)
