import logging
from django.conf import settings
from django.db import models
from django.utils.translation import get_language

logger = logging.getLogger(__name__)

UNIT_CHOICES = [
    ('kg', 'Kilogram'),
    ('piece', 'Piece'),
    ('litre', 'Litre'),
]

class Category(models.Model):
    name_i18n = models.JSONField(default=dict)  # e.g. {"en": "Fruits", "fr": "Fruits"}

    def get_translated_name(self):
        lang = get_language()
        return self.name_i18n.get(lang, self.name_i18n.get("en", ""))

    def __str__(self):
        return self.get_translated_name()


class Product(models.Model):
    name_i18n = models.JSONField(default=dict)
    description_i18n = models.JSONField(default=dict)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    low_stock_threshold = models.PositiveIntegerField(default=5)
    is_rentable = models.BooleanField(default=False)
    unit_of_measure = models.CharField(
        max_length=20,
        choices=UNIT_CHOICES,
        default='piece'
    )
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_products', blank=True)
    views = models.PositiveIntegerField(default=0)

    @property
    def is_available(self):
        return self.stock > 0

    def is_low_stock(self):
        return self.stock <= self.low_stock_threshold

    def check_stock(self):
        if self.is_low_stock():
            logger.warning(f"Low stock alert: {self.name_i18n.get('en', 'Unnamed')} has only {self.stock} left!")

    def get_translated_name(self):
        lang = get_language()
        return self.name_i18n.get(lang, self.name_i18n.get("en", ""))

    def get_translated_description(self):
        lang = get_language()
        return self.description_i18n.get(lang, self.description_i18n.get("en", ""))

    def save(self, *args, **kwargs):
        self.check_stock()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.get_translated_name()


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/')

    def __str__(self):
        return f"Image for {self.product.get_translated_name()}"


class Rental(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def cancel_rental(self):
        if not self.is_active:
            return False
        self.is_active = False
        self.save()
        return True

    def __str__(self):
        return f"{self.user.username} - {self.product.get_translated_name()} ({'Active' if self.is_active else 'Canceled'})"


class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user.username} ❤️ {self.product.get_translated_name()}"
