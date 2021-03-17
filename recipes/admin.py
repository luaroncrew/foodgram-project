from django.contrib import admin
from .models import Recipe, Ingredient, Component, Following, Tag, Favourite, Purchase


admin.site.register(Recipe)
admin.site.register(Following)
admin.site.register(Component)
admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(Favourite)
admin.site.register(Purchase)
