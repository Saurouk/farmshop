from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters
from rest_framework.permissions import IsAuthenticated
from .models import Product, Rental, Category
from .serializers import ProductSerializer, RentalSerializer, CategorySerializer  # Vérifier l'importation correcte

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]  # Protège l'API avec JWT

    # Ajout les options de recherche et filtrage
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category__name']  # Filtrer par nom de catégorie
    search_fields = ['name', 'description']  # Rechercher dans les noms et descriptions

    def get_permissions(self):
        """
        Définir les permissions selon le type de requête :
        - GET (liste des produits) → accessible à tout le monde (y compris non connectés).
        - POST, PUT, DELETE → réservé aux administrateurs.
        """
        if self.request.method == 'GET':
            return [permissions.AllowAny()]  # Tout le monde peut voir la liste des produits
        return [permissions.IsAdminUser()]  # Seul l'admin peut ajouter/modifier/supprimer

# 🚀 Correction : Sortie de `CategoryViewSet` en dehors de `ProductViewSet`
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]  # Seuls les admins peuvent créer/modifier/supprimer

class RentalViewSet(viewsets.ModelViewSet):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    permission_classes = [IsAuthenticated]  # Protège les locations avec JWT
