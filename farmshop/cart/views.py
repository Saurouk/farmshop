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
        """
        Récupérer le contenu du panier pour l'utilisateur connecté
        """
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class AddItemToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Ajouter un produit au panier et ajuster le stock
        """
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product does not exist'}, status=404)

        # Vérifier si le produit est disponible
        if not product.is_available:
            return Response({'error': f"{product.name} is not available."}, status=400)

        # Vérifier si le produit est en rupture de stock
        if product.stock == 0:
            return Response({'error': f"{product.name} is out of stock and cannot be added to cart."}, status=400)

        if quantity > product.stock:
            return Response({'error': f"Only {product.stock} units available."}, status=400)

        cart, created = Cart.objects.get_or_create(user=request.user)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            if item.quantity + quantity > product.stock:
                return Response({'error': f"Exceeds stock. Add only {product.stock - item.quantity} more."}, status=400)
            item.quantity += quantity
        else:
            item.quantity = quantity

        product.stock -= quantity
        product.save()
        item.save()

        # Vérification du seuil critique
        if product.is_low_stock():
            print(f"Low stock alert for {product.name}. Only {product.stock} left.")

        return Response({'message': f"{quantity} unit(s) of {product.name} added to cart."}, status=201)


class RemoveItemFromCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Supprimer un produit du panier et réajuster le stock
        """
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
            product.stock += item.quantity
            product.save()
            item.delete()
        else:
            product.stock += quantity
            product.save()
            item.quantity -= quantity
            item.save()

        return Response({'message': f"Removed {quantity} unit(s) of {product.name} from cart."}, status=200)
