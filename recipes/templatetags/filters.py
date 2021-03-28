from django import template
from django.shortcuts import get_object_or_404

from recipes.models import Favourite, Purchase, Recipe, Following, Tag

register = template.Library()


@register.filter
def is_requested(request, tag):
    return tag in request.GET.getlist('tags')


@register.filter
def make_tag_filtered_url(request, tag):
    requested_tags = request.GET.getlist('tags')
    if tag in requested_tags:
        requested_tags.remove(tag)
    else:
        requested_tags.append(tag)

    return '?tags=' + '&tags='.join(requested_tags) if requested_tags else '.'


@register.filter
def is_favourite(recipe, user):
    return Favourite.objects.filter(user=user, recipe=recipe).count() > 0


@register.filter
def is_wishlisted(recipe, user):
    return Purchase.objects.filter(user=user, recipe=recipe).count() > 0


@register.simple_tag
def get_last_three_recipes(author):
    recipes = []
    for k, recipe in enumerate(Recipe.objects.filter(author=author).reverse()):
        recipes.append(recipe)
        if k == 2:
            break
    return recipes


@register.simple_tag
def recipes_counter(user):
    return Recipe.objects.filter(author=user).count()


@register.filter
def is_subscribed(user, author):
    return Following.objects.filter(user=author, follower=user)


@register.simple_tag
def get_tags_for_url(request):
    tags = request.GET.getlist('tags')
    if tags:
        return '&tags=' + '&tags='.join(tags)
    else:
        return ''


@register.filter
def is_tagged(recipe, tag_pk):
    return get_object_or_404(Tag, pk=tag_pk) in recipe.tags.all()
