from rest_framework import viewsets, permissions, serializers
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
import logging

from .models import Article, Comment, Report
from .serializers import ArticleSerializer, CommentSerializer, ReportSerializer

logger = logging.getLogger(__name__)

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('-created_at')
    serializer_class = ArticleSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def toggle_like(self, request, pk=None):
        article = self.get_object()
        user = request.user
        if user in article.likes.all():
            article.likes.remove(user)
            liked = False
        else:
            article.likes.add(user)
            liked = True
        return Response({'liked': liked, 'likes_count': article.likes.count()})

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.all().order_by('-created_at')
        article_id = self.request.query_params.get('article')
        if article_id:
            queryset = queryset.filter(article__id=article_id)
        return queryset

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def perform_create(self, serializer):
        try:
            user = self.request.user
            logger.info(f"🗨️ Creating comment by user: {user.username} (is_staff={user.is_staff})")
            serializer.save(user=user)
        except Exception as e:
            logger.error(f"❌ Error creating comment: {str(e)}")
            raise

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all().order_by('-created_at')
    serializer_class = ReportSerializer

    def get_permissions(self):
        if self.request.method in ['GET', 'PATCH', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        user = self.request.user
        comment = serializer.validated_data['reported_comment']
        if Report.objects.filter(reporter=user, reported_comment=comment).exists():
            raise serializers.ValidationError({"detail": "Vous avez déjà signalé ce commentaire."})
        serializer.save(reporter=user)

    @action(detail=True, methods=['DELETE'], permission_classes=[permissions.IsAdminUser])
    def delete_reported_comment(self, request, pk=None):
        report = self.get_object()
        comment = report.reported_comment
        if comment:
            comment.delete()
            report.resolved = True
            report.save()
            return Response({"message": "Comment deleted and report resolved."}, status=200)
        return Response({"error": "Commentaire non trouvé."}, status=404)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def list_reported_comments(request):
    reported_comments = Comment.objects.filter(report__isnull=False, report__resolved=False)
    serializer = CommentSerializer(reported_comments, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_reported_comment(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
        return Response({"message": "Commentaire supprimé avec succès."}, status=200)
    except Comment.DoesNotExist:
        return Response({"error": "Commentaire non trouvé."}, status=404)

@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def ignore_report(request, comment_id):
    reports = Report.objects.filter(reported_comment__id=comment_id, resolved=False)
    print("🔍 Nombre de signalements non résolus trouvés :", reports.count())
    if not reports.exists():
        return Response({"error": "Aucun signalement trouvé pour ce commentaire."}, status=404)
    reports.update(resolved=True)
    return Response({"message": "Tous les signalements ont été ignorés avec succès."}, status=200)
