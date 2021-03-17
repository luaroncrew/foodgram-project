from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .forms import RecipeCreationForm
from .models import Recipe, Component, Ingredient, Tag


def index(request):
    tags = request.GET.getlist('tags')
    if tags:
        recipes = Recipe.objects.filter(tags__name__in=tags).distinct()
    else:
        recipes = Recipe.objects.all()
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'paginator': paginator,
        'page': page,
        'page_name': 'index'
    }
    return render(request, 'recipes/index.html', context=context)


def create_recipe(request):
    if request.method == 'POST':
        form = RecipeCreationForm(request.POST)
        if form.is_valid():

            tags = []
            recipe = Recipe.objects.create(
                author=request.user,
                name=form.name,
                picture=form.picture,
                description=form.description,
                prep_time=form.prep_time,
                tags=form.tag,

            )
            recipe.save()
            ingredient = Component.objects.create(
                qnt=form.qnt, Ingredient=form.ingredient, recipe=recipe
            )
            ingredient.save()
            return redirect('index')
    form = RecipeCreationForm()
    return render(request, 'recipes/recipe_creation_page.html', {'form': form, 'page_name': ' create_recipe'})


@login_required
def favourites(request):
    fav_recipes = Recipe.objects.filter(favourites__user=request.user)
    tags = request.GET.getlist('tags')
    if tags:
        recipes = fav_recipes.objects.filter(tags__name__in=tags).distinct()
    else:
        recipes = fav_recipes
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'paginator': paginator,
        'page': page,
        'page_name': 'favourites'
    }
    return render(request, 'recipes/fav.html', context=context)

