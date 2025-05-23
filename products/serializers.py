from rest_framework import serializers
from .models import Product, Rental, Category, Wishlist, ProductImage, UNIT_CHOICES
from django.utils.translation import get_language


class CategorySerializer(serializers.ModelSerializer):
    name_i18n = serializers.JSONField()
    name = serializers.SerializerMethodField()
    name_fr = serializers.SerializerMethodField()
    name_en = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name_i18n', 'name', 'name_fr', 'name_en']

    def get_name(self, obj):
        lang = get_language()
        return obj.name_i18n.get(lang, obj.name_i18n.get('en', ''))

    def get_name_fr(self, obj):
        return obj.name_i18n.get('fr', '')

    def get_name_en(self, obj):
        return obj.name_i18n.get('en', '')


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
    category = CategorySerializer(read_only=True)
    unit_of_measure = serializers.ChoiceField(choices=UNIT_CHOICES, default='piece')
    is_available = serializers.ReadOnlyField()
    image = serializers.ImageField(required=False, allow_null=True)
    images = ProductImageSerializer(many=True, read_only=True)
    images_upload = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    likes_count = serializers.SerializerMethodField()
    liked_by_user = serializers.SerializerMethodField()
    views = serializers.IntegerField(read_only=True)

    name_i18n = serializers.JSONField()
    description_i18n = serializers.JSONField()
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name_i18n', 'description_i18n', 'name', 'description',
            'price', 'stock', 'low_stock_threshold', 'is_available',
            'category_id', 'category', 'unit_of_measure', 'image', 'images',
            'images_upload', 'is_rentable',
            'likes_count', 'liked_by_user', 'views'
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

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_liked_by_user(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            return request.user in obj.likes.all()
        return False

    def get_name(self, obj):
        lang = get_language()
        return obj.name_i18n.get(lang, obj.name_i18n.get('en', ''))

    def get_description(self, obj):
        lang = get_language()
        return obj.description_i18n.get(lang, obj.description_i18n.get('en', ''))


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
