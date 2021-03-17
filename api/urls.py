from django.urls import path

from . import views
from recipes.models import Purchase, Favourite

urlpatterns = [
    path('favourites/', views.Favorites.as_view()),
    path('favourites/<int:id>/', views.Favorites.as_view()),
    path('purchases/', views.Purchases.as_view()),
    path('purchases/<int:id>/', views.Purchases.as_view())
]
# urlpatterns = [
#     path('favourites/', views.AddRemove(model=Favourite).as_view()),
#     path('favourites/<int:id>/', views.AddRemove(model=Favourite).as_view()),
#     path('purchase/', views.AddRemove(model=Purchase).as_view()),
#     path('purchase<int:id>/', views.AddRemove(model=Purchase).as_view())
# ]
