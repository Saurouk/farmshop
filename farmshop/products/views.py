
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, Rental, Category
from .serializers import ProductSerializer, RentalSerializer, CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category__name']
    search_fields = ['name', 'description']

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]

class RentalViewSet(viewsets.ModelViewSet):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')

        # Vérifier si le produit existe
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        # Vérifier si le produit est bien louable
        if not product.is_rentable:
            return Response({'error': 'This product is not available for rent'}, status=status.HTTP_400_BAD_REQUEST)

        # **Vérifier si le produit est en stock**
        if product.stock <= 0:
            return Response({'error': 'Product out of stock.'}, status=status.HTTP_400_BAD_REQUEST)

        # Créer la location
        rental = Rental.objects.create(
            product=product,
            user=request.user,
            start_date=start_date,
            end_date=end_date,
            is_active=True
        )

        return Response({'message': 'Rental created successfully', 'rental_id': rental.id}, status=status.HTTP_201_CREATED)