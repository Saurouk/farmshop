from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, RentalViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'', ProductViewSet, basename="product")  # ✅ Corrigé pour accéder via /api/products/
router.register(r'rentals', RentalViewSet)
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
]
