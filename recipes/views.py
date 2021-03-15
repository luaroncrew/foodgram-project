from django.shortcuts import render
from django.core.paginator import Paginator

from .models import Recipe


def index(request):
    recipes = Recipe.objects.all()
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'paginator': paginator,
        'page': page
    }
    return render(request, 'recipes/index.html', context=context)
