from django.conf import settings
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création
    updated_at = models.DateTimeField(auto_now=True)  # Date de mise à jour
    is_published = models.BooleanField(default=True)  # ✅ Article publié ou non
    is_reported = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")  # Lien avec un article
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création

    def __str__(self):
        return f"Comment by {self.user.username} on {self.article.title}"

class Report(models.Model):
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Qui a signalé
    reported_comment = models.ForeignKey(Comment, on_delete=models.CASCADE)  # Le commentaire signalé
    reason = models.TextField()  # Motif du signalement
    created_at = models.DateTimeField(auto_now_add=True)  # Date du signalement
    resolved = models.BooleanField(default=False)  # ✅ Champ ajouté ici

    def __str__(self):
        return f"{self.reporter.username} reported comment {self.reported_comment.id}"
