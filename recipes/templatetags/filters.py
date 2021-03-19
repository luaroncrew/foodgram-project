from django import template

from recipes.models import Favourite, Purchase, Recipe, Following

register = template.Library()


@register.filter
def is_requested(request, tag):
    if tag in request.GET.getlist('tags'):
        return True
    return False


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
    if Favourite.objects.filter(user=user, recipe=recipe).count() > 0:
        return True
    return False


@register.filter
def is_wishlisted(recipe, user):
    if Purchase.objects.filter(user=user, recipe=recipe).count() > 0:
        return True
    return False


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
    counter = Recipe.objects.filter(author=user).count()
    return counter


@register.filter
def is_subscribed(user, author):
    subscription = Following.objects.filter(user=author, follower=user)
    if subscription:
        return True
    return False


@register.simple_tag
def get_tags_for_url(request):
    tags = request.GET.getlist('tags')
    if tags:
        return '&tags=' + '&tags='.join(tags)
    else:
        return ''





