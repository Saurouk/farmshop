import logging
from rest_framework import viewsets, permissions, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

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
        gallery_files = request.FILES.getlist('gallery')
        for file in gallery_files:
            ProductImage.objects.create(product=product, image=file)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        gallery_files = request.FILES.getlist('gallery')
        for file in gallery_files:
            ProductImage.objects.create(product=product, image=file)
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
        serializer.save(user=self.request.user)
