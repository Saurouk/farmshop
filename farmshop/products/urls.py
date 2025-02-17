from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, RentalViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'rentals', RentalViewSet)
router.register(r'categories', CategoryViewSet, basename='category')


urlpatterns = [
    path('', include(router.urls)),
]
