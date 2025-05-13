from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet,
    RentalViewSet,
    CategoryViewSet,
    WishlistViewSet,
    CreateRentalPaymentIntentView,
    RemoveFromWishlistView,
    delete_main_image,
    delete_product_image,
)

router = DefaultRouter()
router.register(r'wishlist', WishlistViewSet, basename='wishlist')
router.register(r'rentals', RentalViewSet)
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'', ProductViewSet, basename="product")

urlpatterns = [
    path('', include(router.urls)),
    path('rental-payment-intent/', CreateRentalPaymentIntentView.as_view(), name='rental-payment-intent'),
    path('wishlist/<int:product_id>/remove/', RemoveFromWishlistView.as_view(), name='wishlist-remove'),
    path('images/<int:pk>/', delete_product_image),
    path('<int:product_id>/delete-main-image/', delete_main_image),
    path('<int:pk>/toggle-like/', ProductViewSet.as_view({'post': 'toggle_like'}), name='product-toggle-like'),
]
