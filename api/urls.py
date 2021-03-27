from django.urls import path, include

from . import views


api_v1_pattern_list = [
    path('favourites/', views.Favorites.as_view(), name='api_add_favourites'),
    path(
        'favourites/<int:id>/',
        views.Favorites.as_view(),
        name='api_delete_favourites'),
    path('purchases/', views.Purchases.as_view(), name='api_add_purchases'),
    path(
        'purchases/<int:id>/',
        views.Purchases.as_view(),
        name='api_delete_purchases'
    ),
    path(
        'ingredients/',
        views.RecipeCreation.as_view(),
        name='api_get_ingredients'
    ),
    path(
        'subscriptions/',
        views.Subscriptions.as_view(),
        name='api_add_subscription'
    ),
    path(
        'subscriptions/<int:id>/',
        views.Subscriptions.as_view(),
        name='api_delete_subscription'
    ),
]

urlpatterns = [
    path('v1/', include(api_v1_pattern_list)),
]
