from django.urls import path

from . import views


urlpatterns = [
    path('home/', views.index, name='index'),
    path('create/', views.create_recipe, name='create_recipe')
]
