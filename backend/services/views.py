from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model


from .models import Service
from .serializers import ServiceSerializer
from core.permissions import IsAdminOrReadOnly
from core.pagination import DefaultPagination
from core.models import Notification
from core.utils import create_notification


class ServiceViewSet(ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['service_type', 'city']
    search_fields = ['name__icontains', 'service_type__icontains',
                     'city__icontains', 'description__contains']
    ordering_fields = ['id', 'name', 'service_type', 'city']
    lookup_field = 'slug'
    pagination_class = DefaultPagination

    @action(detail=True, methods=['post'], url_path='click', permission_classes=[AllowAny])
    def register_click(self, request, slug=None):
        service = self.get_object()
        user = request.user if request.user.is_authenticated else None

        if user and user.is_staff:
            return Response({'status': 'Click registered'}, status=status.HTTP_200_OK)

        staff_user = get_user_model().objects.filter(is_staff=True).first()
        if not staff_user:
            return Response({'status': 'Click registered'}, status=status.HTTP_200_OK)

        create_notification(
            recipient=staff_user,
            notification_type=Notification.NOTIFICATION_TYPE_AFFILIATE_CLICKED,
            message=f"{user.username if user else 'Anonymous'} clicked on service: {service.name}.",
            content_object=service
        )
        return Response({'status': 'Click registered'}, status=status.HTTP_200_OK)
