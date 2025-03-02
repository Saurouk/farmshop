from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, UserViewSet, MessageViewSet, get_current_user

# ✅ Définition correcte du router pour `/api/users/`
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')  # ✅ Accès à `/api/users/`
router.register(r'messages', MessageViewSet, basename='message')  # ✅ Accès à `/api/users/messages/`

urlpatterns = [
    # ✅ Routes pour l'inscription et la connexion
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', get_current_user, name='get_current_user'),  # ✅ Récupère l'utilisateur connecté

    # ✅ Routes dynamiques des utilisateurs/messages (gérées par `DefaultRouter`)
    path('', include(router.urls)),
]
