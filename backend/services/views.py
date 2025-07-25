from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from .models import Service
from .serializers import ServiceSerializer
from core.permissions import IsAdminOrReadOnly
from core.pagination import DefaultPagination


class ServiceViewSet(ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['service_type', 'city']
    search_fields = ['name__icontains', 'service_type__icontains',
                     'city__icontains', 'description__contains']
    ordering_fields = ['id', 'name', 'service_type', 'city']
    pagination_class = DefaultPagination
