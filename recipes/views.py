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
    }
    return render(request, 'recipes/index.html', context=context)


def create_recipe(request):
    if request.method == 'POST':
        form = RecipeCreationForm(request.POST)
        if form.is_valid():
            recipe = Recipe.objects.create(
                author=request.user,
                name=form.name,
                picture=form.picture,
                description=form.description,
                prep_time=form.prep_time,
                tag=form.tag
            )
            recipe.save()
            ingredient = Component.objects.create(
                qnt=form.qnt, Ingredient=form.ingredient, recipe=recipe
            )
            ingredient.save()
            return redirect('index')
    form = RecipeCreationForm()
    return render(request, 'recipes/formRecipe.html', {'form': form})


@login_required
def favourites(request):
    tags = request.GET.getlist('tags')
    if tags:
        recipes = Recipe.objects.filter(tags__name__in=tags).filter(favourite=request.user).distinct()
    else:
        recipes = Recipe.objects.filter(favourite=request.user)
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'paginator': paginator,
        'page': page,
    }
    return render(request, 'recipes/fav.html', context=context)

