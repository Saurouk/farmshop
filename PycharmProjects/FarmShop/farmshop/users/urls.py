from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, UserViewSet, MessageViewSet, get_current_user, admin_dashboard

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    # ✅ Routes d'authentification
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # ✅ Routes des utilisateurs
    path('me/', get_current_user, name='get_current_user'),
    path('messages/', MessageViewSet.as_view({'get': 'list'}), name='user-messages'),

    # ✅ Route du dashboard admin (corrigée)
    path('dashboard/', admin_dashboard, name='admin_dashboard'),

    # ✅ Ajout des routes dynamiques générées par DefaultRouter
    path('', include(router.urls)),
]
