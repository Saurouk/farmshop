import logging
from django.db import models
from django.contrib.auth.models import User

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
    low_stock_threshold = models.PositiveIntegerField(default=5)
    is_rentable = models.BooleanField(default=False)
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

    @property
    def is_available(self):
        """ Retourne True si le produit est en stock """
        return self.stock > 0

    def check_stock(self):
        """ Vérifie si le stock est bas et log un message """
        if self.stock <= self.low_stock_threshold:
            logger.warning(f"Low stock alert: {self.name} has only {self.stock} left!")

    def save(self, *args, **kwargs):
        """ Vérifie le stock avant de sauvegarder """
        self.check_stock()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Rental(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def cancel_rental(self):
        """ Annuler une location active """
        if not self.is_active:
            return False  # Déjà annulée
        self.is_active = False
        self.save()
        return True

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({'Active' if self.is_active else 'Canceled'})"
