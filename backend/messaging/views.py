import logging
from django.db import transaction
from django.db.models import Q, F, Case, When
from django.db import models
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Message
from .serializers import MessageSerializer, MessageUserSerializer, ConversationSerializer
from core.pagination import DefaultPagination
from core.permissions import MessagePermission


logger = logging.getLogger(__name__)
User = get_user_model()


class MessageViewSet(ModelViewSet):
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['sender_id', 'receiver_id']
    search_fields = ['content']
    ordering_fields = ['id', 'sent_at']
    permission_classes = [IsAuthenticated, MessagePermission]
    # pagination_class = DefaultPagination

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
        """Get all conversations for the current user - OPTIMIZED"""
        user = request.user

        # Get conversations using the optimized manager method
        conversations_data = Message.objects.get_user_conversations(user)

        # Bulk fetch all participant users to avoid N+1 queries
        participant_ids = [conv['other_user_id']
                           for conv in conversations_data]
        participants = User.objects.in_bulk(participant_ids)

        # Bulk fetch latest messages
        latest_message_ids = [conv['latest_message_id']
                              for conv in conversations_data]
        latest_messages = Message.objects.select_related(
            'sender', 'receiver').in_bulk(latest_message_ids)

        result = []
        for conv in conversations_data:
            participant = participants.get(conv['other_user_id'])
            latest_message = latest_messages.get(conv['latest_message_id'])

            if participant:  # Safety check
                result.append({
                    'participant': participant,
                    'latest_message': latest_message,
                    'unread_count': conv['unread_count'],
                    'last_activity': conv['last_activity']
                })

        serializer = ConversationSerializer(
            result, many=True, context={'request': request})
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

        # Order messages by 'sent_at' in descending order
        messages_qs = Message.objects.get_conversation(
            request.user, other_user).order_by('sent_at')

        # Paginate the results
        page = self.paginate_queryset(messages_qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # Reverse the order for the frontend to display chronologically
            return self.get_paginated_response(serializer.data[::-1])

        serializer = self.get_serializer(messages_qs, many=True)
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

    @action(detail=False, methods=['post'], url_path='delete_conversation')
    def delete_conversation(self, request):
        """
        Marks all messages in a conversation as deleted for the current user.
        If messages are deleted by both participants, they are permanently removed.
        """
        other_user_id = request.data.get('user_id')
        user = request.user

        if not other_user_id:
            return Response(
                {'error': 'user_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Verify the other user exists
            User.objects.get(id=other_user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Use transaction for atomicity
        with transaction.atomic():
            # Get conversation messages
            conversation_messages = Message.objects.filter(
                Q(sender=user, receiver_id=other_user_id) |
                Q(sender_id=other_user_id, receiver=user)
            )

            # Update deletion flags
            updated = conversation_messages.update(
                is_deleted_by_sender=Case(
                    When(sender=user, then=True),
                    default=F('is_deleted_by_sender'),
                    output_field=models.BooleanField()
                ),
                is_deleted_by_receiver=Case(
                    When(receiver=user, then=True),
                    default=F('is_deleted_by_receiver'),
                    output_field=models.BooleanField()
                )
            )

            # Delete messages that are now marked as deleted by both users
            # Only delete from this specific conversation
            deleted_count = conversation_messages.filter(
                is_deleted_by_sender=True,
                is_deleted_by_receiver=True
            ).delete()[0]

            logger.info(
                f"User {user.id} deleted conversation with user {other_user_id}. "
                f"Updated {updated} messages, permanently deleted {deleted_count} messages."
            )

        return Response(
            {'status': f'Conversation deleted. {deleted_count} messages permanently removed.'},
            status=status.HTTP_200_OK
        )
