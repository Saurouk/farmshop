from rest_framework import serializers
from .models import Article, Comment, Report

class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')  # Afficher le nom de l'auteur
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)  # Nombre de commentaires

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at', 'is_published', 'comments_count']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    article_title = serializers.ReadOnlyField(source='article.title', read_only=True)
    article = serializers.PrimaryKeyRelatedField(queryset=Article.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'article', 'article_title', 'user', 'content', 'created_at']

class ReportSerializer(serializers.ModelSerializer):
    reporter = serializers.ReadOnlyField(source='reporter.username')
    reported_comment = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all())

    class Meta:
        model = Report
        fields = ['id', 'reporter', 'reported_comment', 'reason', 'created_at', 'resolved']

