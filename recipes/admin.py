from django.contrib import admin
from .models import Recipe, Ingredient, Component, Following


admin.site.register(Recipe)
admin.site.register(Following)
admin.site.register(Component)
admin.site.register(Ingredient)

