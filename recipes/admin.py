from django.contrib import admin

from .models import Recipe, Ingredient, Component, Following, Tag, Favourite, \
    Purchase


class RecipeAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    list_display = ('name', 'author')


class IngredientAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    list_display = ('name', 'measurement')


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Following)
admin.site.register(Component)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag)
admin.site.register(Favourite)
admin.site.register(Purchase)
