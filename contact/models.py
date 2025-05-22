from django.db import models

class ContactMessage(models.Model):
    REASON_CHOICES = [
        ('products', 'Nos produits'),
        ('articles', 'Nos articles'),
        ('other', 'Autres'),
    ]

    email = models.EmailField()
    subject = models.CharField(max_length=255)
    content = models.TextField()
    reason = models.CharField(max_length=50, choices=REASON_CHOICES)
    is_handled = models.BooleanField(default=False)
    response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.email} - {self.subject}"
