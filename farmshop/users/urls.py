from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, UserViewSet, MessageViewSet, get_current_user

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    # ✅ Route d'inscription (elle doit être bien là)
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', get_current_user, name='get_current_user'),
    path('messages/', MessageViewSet.as_view({'get': 'list'}), name='user-messages'),
    path('', include(router.urls)),
]
