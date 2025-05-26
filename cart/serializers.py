from rest_framework import serializers
from .models import Cart, CartItem
from products.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

    def get_product(self, obj):

        return ProductSerializer(obj.product, context=self.context).data


class CartSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price', 'created_at']

    def get_items(self, obj):
        serializer = CartItemSerializer(obj.items.all(), many=True, context=self.context)
        return serializer.data

    def get_total_price(self, obj):
        return obj.total_price()
