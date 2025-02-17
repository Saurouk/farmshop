from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from .models import Article, Comment
from .serializers import ArticleSerializer, CommentSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('-created_at')
    serializer_class = ArticleSerializer

    def get_permissions(self):
        """
        Définir les permissions en fonction de la requête :
        - GET (voir les articles) → accessible à tous (visiteurs et utilisateurs).
        - POST, PUT, DELETE → réservé aux administrateurs.
        - Un utilisateur normal ne peut que voir les articles publiés.
        """
        if self.request.method in ['GET']:
            return [permissions.AllowAny()]  # Tout le monde peut voir les articles
        return [permissions.IsAdminUser()]  # ✅ Seuls les admins peuvent créer/modifier/supprimer

    def perform_create(self, serializer):
        """
        Lorsqu'un article est créé, l'auteur est automatiquement l'utilisateur connecté.
        """
        serializer.save(author=self.request.user)  # ✅ Assigner automatiquement l'auteur

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        """
        Filtrer les commentaires en fonction de l'article passé en paramètre.
        Exemple : /api/comments/?article=1 → Retourne seulement les commentaires de l'article 1.
        """
        queryset = Comment.objects.all().order_by('-created_at')
        article_id = self.request.query_params.get('article')  # Récupérer l'ID de l'article depuis l'URL
        if article_id:
            queryset = queryset.filter(article__id=article_id)  # Filtrer les commentaires par article
        return queryset

    def get_permissions(self):
        """
        Définir les permissions :
        - GET (voir les commentaires) → tout le monde peut voir.
        - POST (ajouter un commentaire) → tous les utilisateurs connectés, y compris les admins.
        - DELETE (supprimer un commentaire) → réservé aux administrateurs.
        """
        if self.request.method in ['GET']:
            return [permissions.AllowAny()]
        elif self.request.method in ['POST']:
            return [permissions.IsAuthenticated()]  # ✅ Permet à tous les utilisateurs connectés (admin et users)
        return [permissions.IsAdminUser()]  # ✅ Seul l'admin peut supprimer

    def perform_create(self, serializer):
        """
        Lorsqu'un commentaire est créé, l'utilisateur connecté est automatiquement défini comme auteur.
        """
        serializer.save(user=self.request.user)
