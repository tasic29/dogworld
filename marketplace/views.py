from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter


from core.pagination import DefaultPagination
from core.permissions import IsAdminOrReadOnly
from .serializers import CategorySerializer, ProductSerializer, TagSerializer
from .models import Product, Category, Tag


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related('category').prefetch_related(
        Prefetch('tags', queryset=Tag.objects.order_by('name'))
    )

    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['created_at', 'category', 'tags']
    search_fields = ['title', 'description', 'tags__name', 'category__name']
    ordering_fields = ['id', 'title', 'price', 'created_at']
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = DefaultPagination


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(products_count=Count('product')).all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'slug']
    search_fields = ['name', 'slug']
    ordering_fields = ['id', 'name']
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = DefaultPagination

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.product_set.exists():
            return Response(
                {'error': 'Cannot delete this category because it has associated products.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['id', 'name']
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = DefaultPagination
