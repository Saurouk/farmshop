from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, UserViewSet, MessageViewSet

# ✅ Définition correcte du router pour les users/messages
router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')  # ✅ Accès à `/api/users/`
router.register(r'messages', MessageViewSet, basename='message')  # ✅ Accès à `/api/users/messages/`

urlpatterns = [
    # ✅ Routes pour l'authentification
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # ✅ Inclure le router pour gérer `/api/users/` et `/api/users/messages/`
    path('', include(router.urls)),
]
