from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    get_current_user,
    list_users,
    delete_user,
    update_user,
    create_user,
    admin_dashboard,
    RegisterView,
    UserViewSet,
    MessageViewSet,
    CustomTokenObtainPairView,
    download_user_data,
    delete_account,
    confirm_email,
)

router = DefaultRouter()
router.register(r'admin/users', UserViewSet, basename='user-admin')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('me/', get_current_user, name='current_user'),
    path('me/download-data/', download_user_data, name='download_user_data'),
    path('list/', list_users, name='list_users'),
    path('delete/<int:user_id>/', delete_user, name='delete_user'),
    path('update/<int:user_id>/', update_user, name='update_user'),
    path('create/', create_user, name='create_user'),
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('download/', download_user_data, name='download_user_data'),
    path('me/delete/', delete_account, name='delete_account'),
    path('confirm/<uidb64>/<token>/', confirm_email, name='confirm_email'),  # ✅ Lien d'activation
    path('', include(router.urls)),
]
