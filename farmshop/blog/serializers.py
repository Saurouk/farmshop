from rest_framework import serializers
from .models import Article, Comment

class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')  # Afficher le nom de l'auteur
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)  # Nombre de commentaires

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at', 'is_published', 'comments_count']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # ✅ Lire le username de l'utilisateur
    article_title = serializers.ReadOnlyField(source='article.title')  # ✅ Affiche le titre de l'article au lieu de son ID

    class Meta:
        model = Comment
        fields = ['id', 'article', 'article_title', 'user', 'content', 'created_at']


