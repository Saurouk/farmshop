from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, RentalViewSet, CategoryViewSet, WishlistViewSet

router = DefaultRouter()
router.register(r'wishlist', WishlistViewSet, basename='wishlist')
router.register(r'rentals', RentalViewSet)
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'', ProductViewSet, basename="product")  # En dernier



urlpatterns = [
    path('', include(router.urls)),
]
