from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from . import spec_pages

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('recipes/', include('recipes.urls')),
    path('api/', include('api.urls')),
    path('about/', spec_pages.about, name='about'),
    path('technologies/', spec_pages.technologies, name='technologies')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
