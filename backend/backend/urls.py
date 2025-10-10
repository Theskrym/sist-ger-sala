from django.contrib import admin
from django.urls import path, include
from spaces.admin_site import admin_site

urlpatterns = [
    path('admin/', admin_site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/', include('spaces.urls')),
]