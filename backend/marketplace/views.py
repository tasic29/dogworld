from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action

from core.models import Notification
from core.utils import create_notification
from core.pagination import DefaultPagination
from core.permissions import IsAdminOrReadOnly
from rest_framework.permissions import AllowAny
from .serializers import CategorySerializer, ProductSerializer
from .models import Product, Category
from .filters import ProductFilter


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related('category').order_by('title')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title__icontains',
                     'description__icontains', 'category__name__icontains']
    ordering_fields = ['id', 'title', 'price', 'created_at']
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = DefaultPagination

    @action(detail=True, methods=['post'], url_path='click', permission_classes=[AllowAny])
    def register_click(self, request, slug=None):
        product = self.get_object()
        user = request.user if request.user.is_authenticated else None

        if user and user.is_staff:
            return Response({'status': 'Click registered'}, status=status.HTTP_200_OK)

        staff_user = get_user_model().objects.filter(is_staff=True).first()
        if not staff_user:
            return Response({'status': 'Click registered'}, status=status.HTTP_200_OK)

        create_notification(
            recipient=staff_user,
            notification_type=Notification.NOTIFICATION_TYPE_AFFILIATE_CLICKED,
            message=f"{user.username if user else 'Anonymous'} clicked on {product.title}.",
            content_object=product
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
