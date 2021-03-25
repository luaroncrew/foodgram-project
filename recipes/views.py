from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.paginator import Paginator
from django.http import FileResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RecipeCreationForm
from .models import Recipe, Component, Ingredient, Tag, Purchase, User


# auxiliary functions
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
            component = Component.objects.create(
                quantity=quantity,
                ingredient=Ingredient.objects.get(name=name),
                recipe=recipe
            )
            component.save()


# main views
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
        recipe = Recipe.objects.create(
            author=request.user,
            name=form.cleaned_data.get('name'),
            picture=form.cleaned_data.get('picture'),
            description=form.cleaned_data.get('description'),
            prep_time=form.cleaned_data.get('prep_time'),
        )
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
    if request.GET.get('delete'):
        instance = get_object_or_404(
            Purchase, recipe__pk=request.GET.get('delete'), user=request.user
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
    author_recipes = Recipe.objects.filter(author=author)
    recipes = get_recipes_by_tags(request, author_recipes)
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
    if request.method == 'POST':
        form = RecipeCreationForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            recipe.tags.clear()
            recipe.ingredients.all().delete()
            save_tags_and_components_from_request(request, recipe)
            return redirect('single_recipe', recipe_pk=recipe.pk)

    form = RecipeCreationForm(instance=recipe)
    context = {
        'page_name': 'create_recipe',
        'form': form,
        'recipe': recipe
    }
    return render(request, 'recipes/recipe_creation_page.html', context)


@login_required
def get_txt_ingredients(request):
    components = Component.objects.filter(recipe__purchases__user=request.user)
    file = open('recipes/wishlist.txt', 'w', encoding='utf-8')
    for component in components:
        line = (f'{component.ingredient.name} - '
                f'{component.qnt} {component.ingredient.measurement} \n'
                )
        file.write(line)
    file.close()
    response = FileResponse(
        open('recipes/wishlist.txt', 'rb'),
        filename='wishlist.txt',
        as_attachment=True
    )
    return response


def page_not_found(request, exception):
    return render(
        request,
        'users/message_page.html',
        {'message': 'Ошибка 404'},
        status=404
    )


def server_error(request):
    return render(
        request,
        'users/message_page.html',
        {'message': 'ошибка 500'},
        status=500
    )
