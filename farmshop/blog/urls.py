from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ArticleViewSet,
    CommentViewSet,
    ReportViewSet,
    list_reported_comments,
    delete_reported_comment,
    ignore_report
)

# Router DRF pour les ViewSets
router = DefaultRouter()
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'reports', ReportViewSet, basename='report')

# ViewSet manuel pour articles
article_list = ArticleViewSet.as_view({'get': 'list'})
article_detail = ArticleViewSet.as_view({'get': 'retrieve'})

urlpatterns = [
    # ✅ Liste des articles accessible via /api/blog/
    path('', article_list, name='blog-list'),

    # ✅ Détail d'un article : /api/blog/<id>/
    path('<int:pk>/', article_detail, name='blog-detail'),

    # ✅ Include des routes générées automatiquement (commentaires, signalements)
    path('', include(router.urls)),

    # ✅ Endpoints d'administration
    path('admin/reported-comments/', list_reported_comments, name='reported-comments'),
    path('admin/delete-comment/<int:comment_id>/', delete_reported_comment, name='delete-comment'),
    path('admin/ignore-report/<int:comment_id>/', ignore_report, name='ignore-report'),
]
