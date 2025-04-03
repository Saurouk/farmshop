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

router = DefaultRouter()
router.register(r'', ArticleViewSet, basename='article')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'reports', ReportViewSet, basename='report')

urlpatterns = [
    path('', include(router.urls)),

    # Endpoints admin personnalisés
    path('admin/reported-comments/', list_reported_comments, name='reported-comments'),
    path('admin/delete-comment/<int:comment_id>/', delete_reported_comment, name='delete-comment'),
    path('admin/ignore-report/<int:comment_id>/', ignore_report, name='ignore-report'),
]
