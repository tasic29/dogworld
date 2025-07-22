from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import ProductViewSet, CategoryViewSet, TagViewSet

router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')
router.register('categories', CategoryViewSet, basename='category')
router.register('tags', TagViewSet, basename='marketplace-tag')

urlpatterns = router.urls
