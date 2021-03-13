from django.urls import path, include

from .views import registration


urlpatterns = [
    path('signup/', registration, name='signup'),
]
