from django.db.models.functions import Greatest, Least
from core.pagination import DefaultPagination
from core.permissions import MessagePermission
from .serializers import MessageSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q, Max
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Message
from .serializers import MessageSerializer, ConversationSerializer
from .permissions import MessagePermission
from core.pagination import DefaultPagination


User = get_user_model()


class MessageViewSet(ModelViewSet):
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['sender_id', 'receiver_id']
    search_fields = ['content']
    ordering_fields = ['id', 'sent_at']
    permission_classes = [IsAuthenticated, MessagePermission]
    pagination_class = DefaultPagination

    def get_queryset(self):
        user = self.request.user
        qs = Message.objects.select_related('sender', 'receiver')

        if user.is_staff:
            return qs.all()

        return qs.filter(
            Q(sender=user, is_deleted_by_sender=False) |
            Q(receiver=user, is_deleted_by_receiver=False)
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'sender_id': self.request.user.id if self.request.user.is_authenticated else None,
        })
        return context

    def perform_destroy(self, instance):
        user = self.request.user
        if instance.sender == user:
            instance.is_deleted_by_sender = True
        elif instance.receiver == user:
            instance.is_deleted_by_receiver = True
        else:
            raise PermissionDenied("You cannot delete this message.")

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
        """Mark a message as read"""
        message = self.get_object()

        if message.receiver != request.user:
            return Response(
                {'error': 'You can only mark messages sent to you as read'},
                status=status.HTTP_403_FORBIDDEN
            )

        if message.is_read:
            return Response(
                {'status': 'Message already marked as read'},
                status=status.HTTP_200_OK
            )

        message.mark_as_read()
        return Response(
            {'status': 'Message marked as read'},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'])
    def conversations(self, request):
        """Get all conversations for the current user"""
        user = request.user

        # Get distinct conversation pairs with latest activity
        conversations = (
            Message.objects.filter(Q(sender=user) | Q(receiver=user))
            .exclude(
                Q(sender=user, is_deleted_by_sender=True) |
                Q(receiver=user, is_deleted_by_receiver=True)
            )
            .annotate(
                user1=Least('sender_id', 'receiver_id'),
                user2=Greatest('sender_id', 'receiver_id'),
            )
            .values('user1', 'user2')
            .annotate(last_activity=Max('sent_at'))
            .order_by('-last_activity')
        )

        conversations_data = []
        for conv in conversations:
            # figure out the "other participant"
            other_id = conv['user1'] if conv['user1'] != user.id else conv['user2']
            participant = User.objects.get(id=other_id)

            # get latest message in this conversation
            latest_message = (
                Message.objects.filter(
                    Q(sender=user, receiver=participant, is_deleted_by_sender=False) |
                    Q(sender=participant, receiver=user,
                      is_deleted_by_receiver=False)
                )
                .order_by('-sent_at')
                .first()
            )

            # count unread messages
            unread_count = Message.objects.filter(
                sender=participant,
                receiver=user,
                is_read=False,
                is_deleted_by_receiver=False
            ).count()

            conversations_data.append({
                'participant': participant,
                'latest_message': latest_message,
                'unread_count': unread_count,
                'last_activity': conv['last_activity']
            })

        serializer = ConversationSerializer(conversations_data, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def conversation(self, request):
        """Get messages in a conversation with a specific user"""
        other_user_id = request.query_params.get('user_id')
        if not other_user_id:
            return Response(
                {'error': 'user_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            other_user = User.objects.get(id=other_user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        messages = Message.objects.get_conversation(request.user, other_user)

        # Mark messages as read if they were sent to current user
        unread_messages = messages.filter(
            receiver=request.user,
            is_read=False
        )
        for message in unread_messages:
            message.mark_as_read()

        # Paginate the results
        page = self.paginate_queryset(messages)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get total unread message count for the current user"""
        count = Message.objects.filter(
            receiver=request.user,
            is_read=False,
            is_deleted_by_receiver=False
        ).count()

        return Response({'unread_count': count})

    @action(detail=False, methods=['post'])
    def mark_conversation_as_read(self, request):
        """Mark all messages in a conversation as read"""
        other_user_id = request.data.get('user_id')
        if not other_user_id:
            return Response(
                {'error': 'user_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            other_user = User.objects.get(id=other_user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Mark all unread messages from this user as read
        updated = Message.objects.filter(
            sender=other_user,
            receiver=request.user,
            is_read=False,
            is_deleted_by_receiver=False
        ).update(is_read=True, read_at=timezone.now())

        return Response({
            'status': f'{updated} messages marked as read'
        })
