from django.contrib import admin  # Import du module admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Active l'accès à l'admin
    path('api/', include('dhtapp.urls')),  # Inclure les URLs de l'application dhtapp
]
