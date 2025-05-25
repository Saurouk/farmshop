from rest_framework import serializers
from .models import Article, Comment, Report
from django.utils.translation import get_language


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    article_title = serializers.ReadOnlyField(source='article.get_translated_title')
    content_i18n = serializers.JSONField()
    content = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'article', 'article_title', 'user', 'content_i18n', 'content', 'created_at']

    def get_content(self, obj):
        request = self.context.get('request')
        lang = request.headers.get('Accept-Language') if request else get_language()
        lang = lang.split('-')[0]  # Normalize e.g. 'fr-FR' → 'fr'
        return obj.content_i18n.get(lang, obj.content_i18n.get('en', ''))


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    thumbnail = serializers.ImageField(required=False, allow_null=True)
    likes_count = serializers.SerializerMethodField()
    liked_by_user = serializers.SerializerMethodField()

    title_i18n = serializers.JSONField()
    content_i18n = serializers.JSONField()
    title = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            'id',
            'title_i18n', 'content_i18n',
            'title', 'content',
            'author',
            'created_at', 'updated_at',
            'is_published',
            'comments_count', 'comments',
            'thumbnail',
            'likes_count', 'liked_by_user',
            'likes',
            'views'
        ]

    def get_title(self, obj):
        lang = self.context.get('language', get_language())
        lang = lang.split('-')[0]
        data = obj.title_i18n or {}
        return data.get(lang, data.get('en', ''))

    def get_content(self, obj):
        lang = self.context.get('language', get_language())
        lang = lang.split('-')[0]
        data = obj.content_i18n or {}
        return data.get(lang, data.get('en', ''))

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_liked_by_user(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False


class ReportSerializer(serializers.ModelSerializer):
    reporter = serializers.ReadOnlyField(source='reporter.username')
    reported_comment = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all())
    comment_content = serializers.SerializerMethodField()
    comment_user = serializers.SerializerMethodField()
    article_title = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = [
            'id', 'reporter', 'reported_comment', 'reason', 'created_at',
            'comment_content', 'comment_user', 'article_title', 'resolved'
        ]

    def get_comment_content(self, obj):
        try:
            lang = self.context.get('request').headers.get('Accept-Language', 'fr')
            return obj.reported_comment.content_i18n.get(lang.split('-')[0], obj.reported_comment.content_i18n.get('en', ''))
        except Exception:
            return "Contenu non disponible"

    def get_comment_user(self, obj):
        try:
            return obj.reported_comment.user.username
        except Exception:
            return "Utilisateur inconnu"

    def get_article_title(self, obj):
        try:
            lang = self.context.get('request').headers.get('Accept-Language', 'fr')
            return obj.reported_comment.article.title_i18n.get(lang.split('-')[0], obj.reported_comment.article.title_i18n.get('en', ''))
        except Exception:
            return "Article inconnu"
