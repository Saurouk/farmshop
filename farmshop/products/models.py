import logging
from django.db import models

logger = logging.getLogger(__name__)

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    UNIT_CHOICES = [
        ('kg', 'Kilogram'),
        ('piece', 'Piece'),
        ('litre', 'Litre'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    low_stock_threshold = models.PositiveIntegerField(default=5)  # Seuil critique par défaut
    is_available = models.BooleanField(default=True)
    unit_of_measure = models.CharField(
        max_length=20,
        choices=UNIT_CHOICES,
        default='piece'
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def is_low_stock(self):
        """ Vérifie si le stock est sous le seuil critique """
        return self.stock <= self.low_stock_threshold

    def check_stock(self):
        """ Vérifie si le stock est bas et log un message """
        if self.is_low_stock():
            logger.warning(f"Low stock alert: {self.name} has only {self.stock} left!")

    def save(self, *args, **kwargs):
        """ Vérifie le stock avant de sauvegarder """
        self.check_stock()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Rental(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
