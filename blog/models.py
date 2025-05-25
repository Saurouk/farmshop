from django.conf import settings
from django.db import models
from django.utils.translation import get_language


class Article(models.Model):
    title_i18n = models.JSONField(default=dict)  # e.g. {"fr": "Titre", "en": "Title"}
    content_i18n = models.JSONField(default=dict)  # e.g. {"fr": "Contenu", "en": "Content"}
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    is_reported = models.BooleanField(default=False)
    thumbnail = models.ImageField(upload_to="blog/thumbnails/", null=True, blank=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_articles', blank=True)
    views = models.PositiveIntegerField(default=0)

    def get_translated_title(self):
        lang = get_language()
        return self.title_i18n.get(lang, self.title_i18n.get('en', ''))

    def get_translated_content(self):
        lang = get_language()
        return self.content_i18n.get(lang, self.content_i18n.get('en', ''))

    def __str__(self):
        return self.get_translated_title()


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_i18n = models.JSONField(default=dict)  # e.g. {"fr": "Commentaire", "en": "Comment"}
    created_at = models.DateTimeField(auto_now_add=True)

    def get_translated_content(self):
        lang = get_language()
        return self.content_i18n.get(lang, self.content_i18n.get("en", ""))

    def __str__(self):
        return f"Comment by {self.user.username} on {self.article.get_translated_title()}"


class Report(models.Model):
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reported_comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.reporter.username} reported comment {self.reported_comment.id}"
