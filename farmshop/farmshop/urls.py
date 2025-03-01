from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # ✅ Routes bien organisées sous `api/`
    path('api/products/', include('products.urls')),  # Produits
    path('api/blog/', include('blog.urls')),  # Blog & Commentaires
    path('api/cart/', include('cart.urls')),  # Panier
    path('api/orders/', include('orders.urls')),  # Commandes

    # ✅ Routes d'authentification et gestion des utilisateurs
    path('api/users/', include('users.urls')),  # Utilisateurs & Authentification
    path('api-auth/', include('rest_framework.urls')),
]
