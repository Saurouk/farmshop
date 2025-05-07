from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, UserViewSet, MessageViewSet, get_current_user, admin_dashboard

router = DefaultRouter()
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    # ✅ Authentification
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # ✅ Utilisateur connecté
    path('me/', get_current_user, name='get_current_user'),

    # ✅ Dashboard admin
    path('dashboard/', admin_dashboard, name='admin_dashboard'),

    # ✅ Toutes les routes ViewSet
    path('', include(router.urls)),
]
