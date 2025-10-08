from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.users.urls')),
    path('api/', include('apps.clients.urls')),  # ← Ajoutez cette ligne
    path('api/', include('apps.fournisseurs.urls')),  # ← Ajoutez cette ligne
    path('api/', include('apps.products.urls')),
]