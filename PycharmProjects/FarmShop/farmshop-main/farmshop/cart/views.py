import traceback
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from products.models import Product
from .serializers import CartSerializer


class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class AddItemToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            product_id = request.data.get('product_id')
            quantity = int(request.data.get('quantity', 1))

            product = Product.objects.get(id=product_id)

            if not product.is_available:
                return Response({'error': f"{product.name} is not available."}, status=400)

            cart, created = Cart.objects.get_or_create(user=request.user)
            item, created = CartItem.objects.get_or_create(cart=cart, product=product)

            total_requested = item.quantity + quantity if not created else quantity

            if total_requested > product.stock:
                return Response({'error': f"Only {product.stock - item.quantity} units available."}, status=400)

            if created:
                item.quantity = quantity
            else:
                item.quantity += quantity

            item.save()

            if product.is_low_stock():
                print(f"Low stock alert for {product.name}. Only {product.stock} left.")

            return Response({'message': f"{quantity} unit(s) of {product.name} added to cart."}, status=201)

        except Product.DoesNotExist:
            return Response({'error': 'Product does not exist'}, status=404)
        except Exception as e:
            print("❌ Une erreur s'est produite lors de l'ajout au panier :")
            traceback.print_exc()
            return Response({'error': str(e)}, status=500)


class RemoveItemFromCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart does not exist'}, status=404)

        try:
            item = CartItem.objects.get(cart=cart, product_id=product_id)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found in cart'}, status=404)

        product = item.product
        if quantity >= item.quantity:
            item.delete()
        else:
            item.quantity -= quantity
            item.save()

        return Response({'message': f"Removed {quantity} unit(s) of {product.name} from cart."}, status=200)
