from django.urls import path

from . import views


urlpatterns = [
    path('home/', views.index, name='index'),
    path('create/', views.create_recipe, name='create_recipe'),
    path('favourites/', views.favourites, name='favourites'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('author/<str:author_username>/', views.author_recipes, name='author_recipes'),
    path('single-recipe/<int:recipe_pk>/', views.single_recipe, name='single_recipe'),
    path('edit-recipe/<int:recipe_pk>', views.edit_recipe, name='edit_recipe'),
    path('download-ingredients/', views.get_txt_ingredients, name='download_ingredients')
]
