import logging
from django.db import transaction, models
from django.db.models import Q, F, Case, When
from django.utils import timezone
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed, PermissionDenied

from .models import Message
from .serializers import MessageSerializer, ConversationSerializer
from .permissions import MessagePermission

logger = logging.getLogger(__name__)
User = get_user_model()


class MessageViewSet(ModelViewSet):
    """
    Handles user-to-user messaging:
    - List / retrieve / send messages
    - Conversations overview
    - Infinite scroll message history
    - Mark as read
    - Delete conversation
    """
    serializer_class = MessageSerializer
    permission_classes = [MessagePermission]
    filterset_fields = ['sender_id', 'receiver_id']
    search_fields = ['content']
    ordering_fields = ['id', 'sent_at']

    def get_queryset(self):
        """Limit messages to those visible by the user."""
        user = self.request.user
        qs = Message.objects.select_related('sender', 'receiver')

        if user.is_staff:
            return qs.all()

        return qs.filter(
            Q(sender=user, is_deleted_by_sender=False) |
            Q(receiver=user, is_deleted_by_receiver=False)
        )

    def get_serializer_context(self):
        """Include sender_id in context for create()."""
        context = super().get_serializer_context()
        if self.request.user.is_authenticated:
            context['sender_id'] = self.request.user.id
        return context

    # ---------------------------
    # Forbidden updates
    # ---------------------------
    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PUT is not allowed for messages.")

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PATCH is not allowed for messages.")

    # ---------------------------
    # Custom actions
    # ---------------------------
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Mark a single message as read."""
        message = self.get_object()

        if message.receiver != request.user:
            return Response(
                {'error': 'You can only mark messages sent to you as read'},
                status=status.HTTP_403_FORBIDDEN
            )

        if message.is_read:
            return Response({'status': 'Already read'}, status=status.HTTP_200_OK)

        message.mark_as_read()
        return Response({'status': 'Message marked as read'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def conversations(self, request):
        """List all conversations for the current user (with latest message + unread count)."""
        user = request.user

        conversations_data = Message.objects.get_user_conversations(user)

        # Bulk fetch users + messages to avoid N+1
        participant_ids = [conv['other_user_id']
                           for conv in conversations_data]
        participants = User.objects.in_bulk(participant_ids)

        latest_ids = [conv['latest_message_id'] for conv in conversations_data]
        latest_messages = Message.objects.select_related(
            'sender', 'receiver').in_bulk(latest_ids)

        results = []
        for conv in conversations_data:
            participant = participants.get(conv['other_user_id'])
            latest_message = latest_messages.get(conv['latest_message_id'])

            if participant and latest_message:
                results.append({
                    'participant': participant,
                    'latest_message': latest_message,
                    'unread_count': conv['unread_count'],
                    'last_activity': conv['last_activity']
                })

        serializer = ConversationSerializer(
            results, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def conversation(self, request):
        """
        Get messages with a specific user.
        Supports infinite scroll with ?before=<message_id>.
        Always returns 20 messages in chronological order.
        """
        other_user_id = request.query_params.get('user_id')
        before_id = request.query_params.get('before')

        if not other_user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            other_user = User.objects.get(id=other_user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        qs = Message.objects.get_conversation(request.user, other_user)

        if before_id:
            qs = qs.filter(id__lt=before_id)

        # Fetch last 20, newest first → reverse to chronological
        messages = list(qs.order_by('-sent_at')[:20])[::-1]

        serializer = self.get_serializer(messages, many=True)
        return Response({
            'results': serializer.data,
            'has_more': qs.count() > 20  # let frontend know if more messages exist
        })

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get total unread messages for the current user."""
        count = Message.objects.filter(
            receiver=request.user,
            is_read=False,
            is_deleted_by_receiver=False
        ).count()
        return Response({'unread_count': count})

    @action(detail=False, methods=['post'])
    def mark_conversation_as_read(self, request):
        """Mark all messages in a conversation as read."""
        other_user_id = request.data.get('user_id')
        if not other_user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            other_user = User.objects.get(id=other_user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        updated = Message.objects.filter(
            sender=other_user,
            receiver=request.user,
            is_read=False,
            is_deleted_by_receiver=False
        ).update(is_read=True, read_at=timezone.now())

        return Response({'status': f'{updated} messages marked as read'})

    @action(detail=False, methods=['post'], url_path='delete_conversation')
    def delete_conversation(self, request):
        """
        Marks all messages in a conversation as deleted for the current user.
        If both participants delete, messages are permanently removed.
        """
        other_user_id = request.data.get('user_id')
        user = request.user

        if not other_user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            User.objects.get(id=other_user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        with transaction.atomic():
            conv_qs = Message.objects.filter(
                Q(sender=user, receiver_id=other_user_id) |
                Q(sender_id=other_user_id, receiver=user)
            )

            conv_qs.update(
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

            deleted_count = conv_qs.filter(
                is_deleted_by_sender=True,
                is_deleted_by_receiver=True
            ).delete()[0]

            logger.info(
                f"User {user.id} deleted conversation with user {other_user_id}. "
                f"Permanently deleted {deleted_count} messages."
            )

        return Response(
            {'status': f'Conversation deleted. {deleted_count} messages permanently removed.'},
            status=status.HTTP_200_OK
        )
