"""
URL configuration for crop_project project.
"""
from django.contrib import admin
from django.urls import path, include
from core.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('crops/', include('crops.urls')),
    path('users/', include('users.urls')),
    path('accounts/', include('users.urls')), # Map accounts/ to users/ for default redirects if needed, or just rely on settings
    path('', include('pwa.urls')),
    # path('farms/', include('farms.urls')), # TODO: Implement farms urls
    # path('markets/', include('markets.urls')), # TODO: Implement markets urls
]
