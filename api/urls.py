from django.urls import path

from . import views
from recipes.models import Purchase, Favourite

urlpatterns = [
    path('favourites/', views.Favorites.as_view()),
    path('favourites/<int:id>/', views.Favorites.as_view()),
    path('purchases/', views.Purchases.as_view()),
    path('purchases/<int:id>/', views.Purchases.as_view()),
    path('ingredients/', views.RecipeCreation.as_view()),
    path('subscriptions/', views.Subscriptions.as_view()),
    path('subscriptions/<int:id>/', views.Subscriptions.as_view()),
]
