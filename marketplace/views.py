from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAdminUser

from core.pagination import DefaultPagination
from .permissions import IsAdminOrReadOnly
from .serializers import CategorySerializer, ProductSerializer, TagSerializer
from .models import Product, Category, Tag


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().select_related(
        'category').prefetch_related('tags')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['created_at', 'category', 'tags']
    search_fields = ['title', 'description', 'tags__name', 'category__name']
    ordering_fields = ['id', 'title', 'price', 'created_at']
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = DefaultPagination


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'slug']
    search_fields = ['name', 'slug']
    ordering_fields = ['id', 'name']
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = DefaultPagination


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['id', 'name']
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = DefaultPagination
