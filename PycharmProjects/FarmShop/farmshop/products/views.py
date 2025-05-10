import logging
import stripe
from datetime import datetime
from rest_framework import viewsets, permissions, status, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from django.conf import settings
from .models import Product, Rental, Category, Wishlist, ProductImage
from .serializers import (
    ProductSerializer,
    RentalSerializer,
    CategorySerializer,
    WishlistSerializer,
)

logger = logging.getLogger(__name__)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'stock']
    parser_classes = (MultiPartParser, FormParser)

    def get_permissions(self):
        if self.request.method in ['GET']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]

    def get_permissions(self):
        if self.request.method in ['GET']:
            return [permissions.AllowAny()]
        return super().get_permissions()


class RentalViewSet(viewsets.ModelViewSet):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        if not product.is_rentable:
            return Response({'error': 'This product is not available for rent'}, status=status.HTTP_400_BAD_REQUEST)

        if product.stock <= 0:
            return Response({'error': 'Product out of stock.'}, status=status.HTTP_400_BAD_REQUEST)

        rental = Rental.objects.create(
            product=product,
            user=request.user,
            start_date=start_date,
            end_date=end_date,
            is_active=True
        )

        return Response({'message': 'Rental created successfully', 'rental_id': rental.id}, status=status.HTTP_201_CREATED)


class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        try:
            instance = serializer.save(user=self.request.user)
            print(f"✅ Wishlist item créé : {instance}")
        except IntegrityError:
            print(f"❌ Produit déjà dans la wishlist.")
            raise ValidationError({"non_field_errors": ["Vous avez déjà ajouté ce produit à votre wishlist."]})
        except Exception as e:
            print(f"❌ Erreur inattendue dans perform_create: {e}")
            raise ValidationError({"detail": str(e)})


class RemoveFromWishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, product_id):
        try:
            wishlist_item = Wishlist.objects.get(user=request.user, product__id=product_id)
            wishlist_item.delete()
            return Response({"message": "Produit retiré de la wishlist."}, status=204)
        except Wishlist.DoesNotExist:
            return Response({"error": "Produit non trouvé dans votre wishlist."}, status=404)


class CreateRentalPaymentIntentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        start_date = request.data.get("start_date")
        end_date = request.data.get("end_date")

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Produit introuvable"}, status=404)

        if not product.is_rentable or not product.stock > 0:
            return Response({"error": "Produit non disponible à la location"}, status=400)

        try:
            d1 = datetime.strptime(start_date, "%Y-%m-%d").date()
            d2 = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": "Dates invalides"}, status=400)

        if d2 <= d1:
            return Response({"error": "La date de fin doit être après la date de début"}, status=400)

        days = (d2 - d1).days
        if not hasattr(product, 'daily_price') or not product.daily_price:
            return Response({"error": "Prix journalier non défini pour ce produit"}, status=400)

        total_amount = int(product.daily_price * days * 100)

        stripe.api_key = settings.STRIPE_SECRET_KEY

        try:
            intent = stripe.PaymentIntent.create(
                amount=total_amount,
                currency="usd",
                metadata={
                    "user_id": request.user.id,
                    "product_id": product.id,
                    "start_date": str(start_date),
                    "end_date": str(end_date)
                }
            )
            return Response({"client_secret": intent.client_secret})
        except Exception as e:
            return Response({"error": str(e)}, status=500)

#  suppression image secondaire
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_product_image(request, pk):
    try:
        image = ProductImage.objects.get(pk=pk)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except ProductImage.DoesNotExist:
        return Response({'error': 'Image non trouvée'}, status=status.HTTP_404_NOT_FOUND)

# suppression image principale
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_main_image(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
        product.image.delete(save=True)
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Product.DoesNotExist:
        return Response({'error': 'Produit non trouvé'}, status=status.HTTP_404_NOT_FOUND)
