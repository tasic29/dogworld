from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action

from messaging.models import Notification
from core.pagination import DefaultPagination
from core.permissions import IsAdminOrReadOnly
from .serializers import CategorySerializer, ProductSerializer
from .models import Product, Category


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related('category').order_by('title')

    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['created_at', 'category']
    search_fields = ['title__icontains',
                     'description__icontains', 'category__name__icontains']
    ordering_fields = ['id', 'title', 'price', 'created_at']
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = DefaultPagination

    @action(detail=True, methods=['post'], url_path='click')
    def register_click(self, request, pk=None):
        product = self.get_object()
        user = request.user if request.user.is_authenticated else None

        Notification.objects.create(
            recipient=get_user_model().objects.filter(is_staff=True).first(),
            notification_type=Notification.NOTIFICATION_TYPE_AFFILIATE_CLICKED,
            message=f"{user.username if user else 'Anonymous'} clicked on {product.title}.",
            content_type=ContentType.objects.get_for_model(product),
            object_id=product.id
        )
        return Response({'status': 'Click registered'}, status=status.HTTP_200_OK)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(products_count=Count('product')).all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'slug']
    search_fields = ['name__icontains', 'slug__icontains']
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
