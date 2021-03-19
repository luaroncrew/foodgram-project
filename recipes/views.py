from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


from .forms import RecipeCreationForm
from .models import Recipe, Component, Ingredient, Tag, Purchase, User


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


@login_required
def create_recipe(request):
    if request.method == 'POST':
        print(request.POST)
        form = RecipeCreationForm(request.POST, request.FILES)
        if form.is_valid():
            tags = {'breakfast': 1, 'lunch': 2, 'dinner': 3}
            tags_to_add = []
            for tag in tags.keys():
                if request.POST.get(tag):
                    tags_to_add.append(Tag.objects.get(pk=tags[tag]))

            recipe = Recipe.objects.create(
                author=request.user,
                name=form.cleaned_data.get('name'),
                picture=form.cleaned_data.get('picture'),
                description=form.cleaned_data.get('description'),
                prep_time=form.cleaned_data.get('prep_time'),
            )
            for tag in tags_to_add:
                recipe.tags.add(tag)
            recipe.save()

            for data in request.POST.keys():
                if data.startswith('nameIngredient'):
                    number = data.split('nameIngredient')[1]
                    name = request.POST[data]
                    qnt = int(request.POST[f'valueIngredient{number}'][0])
                    component = Component.objects.create(
                        qnt=qnt,
                        ingredient=Ingredient.objects.get(name=name),
                        recipe=recipe
                    )
                    component.save()
                    return redirect('index')

    form = RecipeCreationForm()
    return render(request, 'recipes/recipe_creation_page.html', {'form': form, 'page_name': 'create_recipe'})


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


@login_required
def wishlist(request):
    if request.GET.get('delete'):
        instance = Purchase.objects.get(recipe__pk=request.GET.get('delete'), user=request.user)
        instance.delete()
    recipes = Recipe.objects.filter(purchases__user=request.user)
    return render(request, 'recipes/wishlist.html', {'recipes': recipes, 'page_name': 'wishlist'})


@login_required
def subscriptions(request):
    users = User.objects.filter(followed_by__follower=request.user)
    paginator = Paginator(users, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'paginator': paginator,
        'page': page,
        'page_name': 'subscriptions'
    }
    return render(request, 'recipes/subscriptions.html', context)


def author_recipes(request, author_username):
    tags = request.GET.getlist('tags')
    author = get_object_or_404(User, username=author_username)
    recipes = Recipe.objects.filter(author=author)
    if tags:
        queryset = recipes.filter(tags__name__in=tags).distinct()
    else:
        queryset = recipes

    paginator = Paginator(queryset, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'author': author,
        'paginator': paginator,
        'page': page,
        'page_name': 'index'
    }
    return render(request, 'recipes/author_page.html', context=context)

