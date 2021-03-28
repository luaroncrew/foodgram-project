from django.conf import settings
from django.shortcuts import get_object_or_404

from .models import Tag, Component, Ingredient


def get_recipes_by_tags(request, queryset):
    tags = request.GET.getlist('tags')
    if tags:
        return queryset.filter(tags__name__in=tags).distinct()
    return queryset


def save_tags_and_components_from_request(request, recipe):
    tags = settings.TAGS
    tags_to_add = []
    for tag in tags.keys():
        if request.POST.get(tag):
            tags_to_add.append(Tag.objects.get(pk=tags[tag]))
    for tag in tags_to_add:
        recipe.tags.add(tag)
    recipe.save()

    for data in request.POST.keys():
        if data.startswith('nameIngredient'):
            number = data.split('nameIngredient')[1]
            name = request.POST[data]
            quantity = int(request.POST[f'valueIngredient{number}'])
            if quantity > 0:
                component = Component.objects.create(
                    quantity=quantity,
                    ingredient=get_object_or_404(Ingredient, name=name),
                    recipe=recipe
                )
                component.save()
