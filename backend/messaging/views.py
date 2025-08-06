from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.decorators import action
from rest_framework import status


from .models import Message
from .serializers import MessageSerializer
from core.permissions import MessagePermission
from core.pagination import DefaultPagination


class MessageViewSet(ModelViewSet):
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['sender_id', 'receiver_id']
    search_fields = ['content']
    ordering_fields = ['id', 'sent_at']
    permission_classes = [MessagePermission]
    pagination_class = DefaultPagination

    def get_queryset(self):
        user = self.request.user
        qs = Message.objects.select_related(
            'sender', 'receiver').all()

        if self.request.user.is_staff:
            return qs

        return qs.filter(
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

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PUT is not allowed for messages.")

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PATCH is not allowed for messages.")

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        message = self.get_object()

        self.check_object_permissions(request, message)

        if message.receiver != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        if message.is_read:
            return Response({'status': 'Message already read'}, status=status.HTTP_200_OK)

        message.is_read = True
        message.save()
        return Response({'status': 'Message marked as read'}, status=status.HTTP_200_OK)
