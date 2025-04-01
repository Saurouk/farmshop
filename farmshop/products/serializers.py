from rest_framework import serializers
from .models import Product, Rental, Category, Wishlist


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']  # Champs à afficher pour les catégories

class ProductSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    category = serializers.StringRelatedField(read_only=True)
    unit_of_measure = serializers.ChoiceField(
        choices=Product.UNIT_CHOICES,
        default='piece'
    )
    is_available = serializers.ReadOnlyField()  # ✅ Champs dynamique, pas stocké en base

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'stock',
            'low_stock_threshold',  # ✅ Champ toujours présent
            'is_available', 'category_id', 'category', 'unit_of_measure'
        ]

class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = '__all__'

class WishlistSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        write_only=True
    )

    class Meta:
        model = Wishlist
        fields = ['id', 'product', 'product_id', 'added_at']

    def create(self, validated_data):
        product = validated_data.pop('product_id')  # On récupère l'ID réel
        return Wishlist.objects.create(product=product, **validated_data)