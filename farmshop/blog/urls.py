from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, CommentViewSet, ReportViewSet

router = DefaultRouter()
router.register(r'blog', ArticleViewSet, basename='article')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'reports', ReportViewSet)  # ✅ Ajout de la route pour les signalements

urlpatterns = [
    path('', include(router.urls)),
    path('reports/<int:pk>/delete_reported_comment/', ReportViewSet.as_view({'delete': 'delete_reported_comment'})),
]
