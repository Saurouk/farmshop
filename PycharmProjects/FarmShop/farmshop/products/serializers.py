# products/serializers.py

from rest_framework import serializers
from .models import Product, Rental, Category, Wishlist, ProductImage, UNIT_CHOICES

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

class ProductSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    category = serializers.StringRelatedField(read_only=True)
    unit_of_measure = serializers.ChoiceField(choices=UNIT_CHOICES, default='piece')
    is_available = serializers.ReadOnlyField()
    image = serializers.ImageField(required=False, allow_null=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'stock',
            'low_stock_threshold', 'is_available', 'category_id',
            'category', 'unit_of_measure', 'image', 'images', 'is_rentable'
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
        product = validated_data.pop('product_id')
        return Wishlist.objects.create(product=product, **validated_data)
