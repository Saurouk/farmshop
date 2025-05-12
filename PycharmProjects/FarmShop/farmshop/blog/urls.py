from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from .views import (
    ArticleViewSet,
    CommentViewSet,
    ReportViewSet,
    list_reported_comments,
    delete_reported_comment,
    ignore_report
)
from .models import Article
from .serializers import ArticleSerializer

router = DefaultRouter()
router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'reports', ReportViewSet, basename='report')

@api_view(['GET'])
@permission_classes([AllowAny])
def blog_root_redirect(request):
    articles = Article.objects.all().order_by('-created_at')
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)

urlpatterns = [
    path('', blog_root_redirect, name='blog-root'),
    path('', include(router.urls)),
    path('admin/reported-comments/', list_reported_comments, name='reported-comments'),
    path('admin/delete-comment/<int:comment_id>/', delete_reported_comment, name='delete-comment'),
    path('admin/ignore-report/<int:comment_id>/', ignore_report, name='ignore-report'),
]
