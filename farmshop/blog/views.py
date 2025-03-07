from rest_framework import viewsets, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .models import Article, Comment, Report
from .serializers import ArticleSerializer, CommentSerializer, ReportSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('-created_at')
    serializer_class = ArticleSerializer

    def get_permissions(self):
        """Définir les permissions en fonction de la requête."""
        if self.request.method == 'GET':
            return [permissions.AllowAny()]  # Tout le monde peut voir les articles
        return [permissions.IsAdminUser()]  # Seuls les admins peuvent créer/modifier/supprimer

    def perform_create(self, serializer):
        """Lorsqu'un article est créé, l'auteur est automatiquement l'utilisateur connecté."""
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        """Filtrer les commentaires en fonction de l'article passé en paramètre."""
        queryset = Comment.objects.all().order_by('-created_at')
        article_id = self.request.query_params.get('article')
        if article_id:
            queryset = queryset.filter(article__id=article_id)
        return queryset

    def get_permissions(self):
        """Définir les permissions pour la gestion des commentaires."""
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]  # Seul l'admin peut supprimer

    def perform_create(self, serializer):
        """Lorsqu'un commentaire est créé, l'utilisateur connecté est automatiquement défini comme auteur."""
        serializer.save(user=self.request.user)


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all().order_by('-created_at')
    serializer_class = ReportSerializer

    def get_permissions(self):
        """Seuls les admins peuvent voir et gérer les signalements."""
        if self.request.method in ['GET', 'PATCH', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        """L'utilisateur connecté est automatiquement défini comme le reporter."""
        serializer.save(reporter=self.request.user)

    @action(detail=True, methods=['DELETE'], permission_classes=[permissions.IsAdminUser])
    def delete_reported_comment(self, request, pk=None):
        """Supprime le commentaire signalé et marque le signalement comme traité."""
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
    """✅ Endpoint pour voir tous les commentaires signalés."""
    reported_comments = Comment.objects.filter(report__isnull=False, report__resolved=False)
    serializer = CommentSerializer(reported_comments, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_reported_comment(request, comment_id):
    """✅ Endpoint pour supprimer un commentaire signalé."""
    try:
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
        return Response({"message": "Commentaire supprimé avec succès."}, status=200)
    except Comment.DoesNotExist:
        return Response({"error": "Commentaire non trouvé."}, status=404)


@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def ignore_report(request, comment_id):
    """✅ Endpoint pour ignorer un signalement."""
    try:
        report = Report.objects.get(reported_comment__id=comment_id, resolved=False)
        report.resolved = True
        report.save()
        return Response({"message": "Signalement ignoré avec succès."}, status=200)
    except Report.DoesNotExist:
        return Response({"error": "Signalement non trouvé."}, status=404)
