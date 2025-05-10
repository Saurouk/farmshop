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
    images_upload = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'stock',
            'low_stock_threshold', 'is_available', 'category_id',
            'category', 'unit_of_measure', 'image', 'images',
            'images_upload', 'is_rentable'
        ]

    def create(self, validated_data):
        images_data = validated_data.pop('images_upload', [])
        product = super().create(validated_data)
        for img in images_data:
            ProductImage.objects.create(product=product, image=img)
        return product

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images_upload', [])
        product = super().update(instance, validated_data)
        for img in images_data:
            ProductImage.objects.create(product=product, image=img)
        return product

class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = '__all__'

class WishlistSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        write_only=True
    )
    product_detail = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'product', 'product_detail', 'added_at']

    def create(self, validated_data):
        return Wishlist.objects.create(**validated_data)
