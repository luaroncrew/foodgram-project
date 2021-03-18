from django.urls import path

from . import views


urlpatterns = [
    path('home/', views.index, name='index'),
    path('create/', views.create_recipe, name='create_recipe'),
    path('favourites/', views.favourites, name='favourites'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('subscriptions/', views.subscriptions, name='subscriptions')
]
