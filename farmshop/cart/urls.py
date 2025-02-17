from django.urls import path
from .views import CartViewSet, AddItemToCartView, RemoveItemFromCartView

urlpatterns = [
    path('', CartViewSet.as_view({'get': 'list'}), name='cart'),  # GET pour afficher le panier
    path('add_item/', AddItemToCartView.as_view(), name='cart-add'),  # POST pour ajouter un produit
    path('remove_item/', RemoveItemFromCartView.as_view(), name='cart-remove'),  # POST pour supprimer un produit
]
