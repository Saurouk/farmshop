from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # ✅ Routes API organisées
    path('api/products/', include('products.urls')),
    path('api/blog/', include('blog.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/orders/', include('orders.urls')),

    # ✅ Routes d'authentification
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # ✅ Ajout de l'authentification et des utilisateurs
    path('api/users/', include('users.urls')),  # ✅ Correct ! Accessible sous /api/users/

    # API Django REST Framework (authentification basique)
    path('api-auth/', include('rest_framework.urls')),
]
