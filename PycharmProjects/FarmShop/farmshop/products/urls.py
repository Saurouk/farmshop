from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, RentalViewSet, CategoryViewSet, WishlistViewSet, CreateRentalPaymentIntentView

router = DefaultRouter()
router.register(r'wishlist', WishlistViewSet, basename='wishlist')
router.register(r'rentals', RentalViewSet)
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'', ProductViewSet, basename="product")

urlpatterns = [
    path('', include(router.urls)),
    path('rental-payment-intent/', CreateRentalPaymentIntentView.as_view(), name='rental-payment-intent'),
]
