from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RecipeCreationForm
from .models import Recipe, Component, Purchase, User
from .utils import get_recipes_by_tags, save_tags_and_components_from_request


def index(request):
    recipes = get_recipes_by_tags(request, Recipe.objects.all())
    paginator = Paginator(recipes.order_by('-pk'), settings.PAGINATE_BY)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'paginator': paginator,
        'page': page,
        'page_name': 'index'
    }
    return render(request, 'recipes/index.html', context=context)


@login_required
def create_recipe(request):
    form = RecipeCreationForm(request.POST or None, request.FILES)
    if form.is_valid():
        form.instance.author = request.user
        recipe = form.save()
        save_tags_and_components_from_request(request, recipe)
        return redirect('single_recipe', recipe_pk=recipe.pk)

    return render(
        request,
        'recipes/recipe_creation_page.html',
        {'form': form, 'page_name': 'create_recipe'}
    )


@login_required
def favourites(request):
    fav_recipes = Recipe.objects.filter(favourites__user=request.user)
    recipes = get_recipes_by_tags(request, fav_recipes)
    paginator = Paginator(recipes, settings.PAGINATE_BY)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'paginator': paginator,
        'page': page,
        'page_name': 'favourites'
    }
    return render(request, 'recipes/fav.html', context=context)


@login_required
def wishlist(request):
    recipe_pk = request.GET.get('delete')
    if recipe_pk:
        instance = get_object_or_404(
            Purchase, recipe__pk=recipe_pk, user=request.user
        )
        instance.delete()
    recipes = Recipe.objects.filter(purchases__user=request.user)
    return render(
        request,
        'recipes/wishlist.html',
        {'recipes': recipes, 'page_name': 'wishlist'}
    )


@login_required
def subscriptions(request):
    users = User.objects.filter(followed_by__follower=request.user)
    paginator = Paginator(users, settings.PAGINATE_BY)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'paginator': paginator,
        'page': page,
        'page_name': 'subscriptions'
    }
    return render(request, 'recipes/subscriptions.html', context)


def author_recipes(request, author_username):
    author = get_object_or_404(User, username=author_username)
    queryset = Recipe.objects.filter(author=author)
    recipes = get_recipes_by_tags(request, queryset)
    paginator = Paginator(recipes, settings.PAGINATE_BY)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'author': author,
        'paginator': paginator,
        'page': page,
        'page_name': 'index'
    }
    return render(request, 'recipes/author_page.html', context=context)


def single_recipe(request, recipe_pk):
    recipe = get_object_or_404(Recipe, pk=recipe_pk)
    context = {
        'recipe': recipe,
        'page_name': 'index'
    }
    return render(request, 'recipes/recipe_page.html', context=context)


@login_required
def edit_recipe(request, recipe_pk):
    recipe = get_object_or_404(Recipe, pk=recipe_pk)
    form = RecipeCreationForm(
        request.POST or None, request.FILES or None, instance=recipe
    )
    if form.is_valid():
        recipe = form.save()
        recipe.tags.clear()
        recipe.ingredients.all().delete()
        save_tags_and_components_from_request(request, recipe)
        return redirect('single_recipe', recipe_pk=recipe.pk)

    context = {
        'page_name': 'create_recipe',
        'form': form,
        'recipe': recipe
    }
    return render(request, 'recipes/recipe_creation_page.html', context)


@login_required
def get_txt_ingredients(request):
    components = Component.objects.filter(recipe__purchases__user=request.user)
    file = ''
    for component in components:
        line = (f'{component.ingredient.name} - '
                f'{component.quantity} {component.ingredient.measurement} \n')
        file += line
    response = HttpResponse(file, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=wishlist.txt'
    return response


@login_required
def delete_recipe(recipe_pk):
    recipe = get_object_or_404(Recipe, pk=recipe_pk)
    recipe.delete()
    return redirect('index')