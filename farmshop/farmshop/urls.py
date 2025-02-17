from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('products.urls')), # Ajout des routes Pour la liste des produits
    path('auth/', include('users.urls')),  # Ajout des routes d'authentification
    path('api/', include('blog.urls')),  # Ajout des routes pour le blog et les commentaires
    path('api/cart/', include('cart.urls')),  # Ajout des routes pour le panier
    path('api/orders/', include('orders.urls')), # Ajout des routes pour les commandes
    path('api-auth/', include('rest_framework.urls')),
]
