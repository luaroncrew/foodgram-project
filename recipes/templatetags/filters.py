from django import template

from recipes.models import Favourite

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

