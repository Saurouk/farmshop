from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="+",  # ✅ Corrige le conflit de relation
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="+",  # ✅ Corrige le conflit de relation
        blank=True
    )

    def __str__(self):
        return self.username

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # ✅ Permet de marquer un message comme lu

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient}"
