from rest_framework import serializers
from .models import Product, Rental, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']  # Champs à afficher pour les catégories


class ProductSerializer(serializers.ModelSerializer):
    # Liaison avec la catégorie (lecture et écriture)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),  # Liste des catégories disponibles
        source='category',  # Le champ de modèle correspondant
        write_only=True  # Ce champ est utilisé uniquement lors des requêtes POST/PUT
    )
    category = serializers.StringRelatedField(read_only=True)  # Affiche le nom de la catégorie dans les réponses

    # Affichage des choix disponibles pour l'unité de mesure
    unit_of_measure = serializers.ChoiceField(
        choices=Product.UNIT_CHOICES,  # Options disponibles définies dans le modèle
        default='piece'
    )

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'stock',
            'is_available', 'category_id', 'category', 'unit_of_measure'
        ]


class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = '__all__'
