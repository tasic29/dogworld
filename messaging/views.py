from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import Message, Notification
from .serializers import MessageSerializer, NotificationSerializer
from core.permissions import MessagePermission
from core.pagination import DefaultPagination


class MessageViewSet(ModelViewSet):
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['sender_id', 'receiver_id']
    search_fields = ['sender__username__icontains',
                     'receiver__username__icontains']
    ordering_fields = ['id', 'sent_at']
    permission_classes = [MessagePermission]
    pagination_class = DefaultPagination

    def get_queryset(self):
        user = self.request.user
        if self.request.user.is_staff:
            return Message.objects.all()
        return Message.objects.filter(
            Q(sender=user, is_deleted_by_sender=False) |
            Q(receiver=user, is_deleted_by_receiver=False)
        )

    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication required.'}, status=401)
        return super().list(request, *args, **kwargs)

    def get_serializer_context(self):
        return {
            'sender_id': self.request.user.id,
        }

    def perform_destroy(self, instance):
        user = self.request.user

        if instance.sender == user:
            instance.is_deleted_by_sender = True
        elif instance.receiver == user:
            instance.is_deleted_by_receiver = True
        else:
            raise PermissionDenied("You can't delete this message.")

        if instance.is_deleted_by_sender and instance.is_deleted_by_receiver:
            instance.delete()
        else:
            instance.save()


class NotificationViewSet(ModelViewSet):
    serializer_class = NotificationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ['id', 'created_at']

    def get_queryset(self):
        if self.request.user.is_staff:
            return Notification.objects.all()

        return Notification.objects.filter(recipient=self.request.user)
