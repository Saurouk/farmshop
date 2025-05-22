from rest_framework import serializers
from .models import Cart, CartItem
from products.serializers import ProductSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # Inclure les détails du produit dans le panier

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']  # Inclure le prix total pour chaque article

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)  # Inclure les articles du panier
    total_price = serializers.SerializerMethodField()  # Calcul dynamique du prix total
    user = serializers.ReadOnlyField(source='user.username')  # Affiche le username au lieu de l'ID

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price', 'created_at']

    def get_total_price(self, obj):
        """
        Calculer le prix total de tous les articles du panier
        """
        return obj.total_price()

