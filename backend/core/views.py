from .models import MyUser  # Assuming MyUser is your custom user model
from .serializers import PublicUserSerializer
from .serializers import NotificationSerializer, PublicUserSerializer
from .models import Notification, MyUser
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status

import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_users(request):
    """
    Search for users by username, email, first_name, or last_name
    """
    query = request.GET.get('query', '').strip()

    # Minimum 3 characters required
    if len(query) < 3:
        return Response({
            'results': [],
            'message': 'Please enter at least 3 characters to search.'
        })

    # Search across multiple fields using '__icontains'
    users = MyUser.objects.filter(
        Q(username__icontains=query) |
        Q(email__icontains=query) |
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query)
    ).filter(
        is_active=True  # Only return active users
    ).exclude(
        id=request.user.id  # Exclude the current user
    ).distinct()[:20]  # Limit to 20 results

    # Serialize the results
    serializer = PublicUserSerializer(
        users, many=True, context={'request': request})

    return Response({
        'results': serializer.data,
        'count': len(serializer.data)
    })


class PublicUserDetailView(generics.RetrieveAPIView):
    queryset = MyUser.objects.all()
    serializer_class = PublicUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'username'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class NotificationViewSet(ModelViewSet):
    serializer_class = NotificationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ['id', 'created_at']
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        if self.request.user.is_staff:
            return Notification.objects.all()
        return Notification.objects.filter(recipient=self.request.user)

    @action(detail=True, methods=['patch'])
    def mark_as_read(self, request, pk=None):
        # Debug logging
        logger.info(f"User: {request.user}, User ID: {request.user.id}")
        logger.info(f"Notification ID: {pk}")

        try:
            notification = self.get_object()
            logger.info(
                f"Notification recipient: {notification.recipient}, Recipient ID: {notification.recipient.id}")
            logger.info(
                f"User matches recipient: {notification.recipient == request.user}")
            logger.info(
                f"User ID matches recipient ID: {notification.recipient.id == request.user.id}")
        except Exception as e:
            logger.error(f"Error getting notification: {e}")
            return Response({'error': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if user has permission to mark this notification as read
        if notification.recipient.id == request.user.id:
            if not notification.is_read:
                notification.is_read = True
                notification.save()
                logger.info(f"Notification {pk} marked as read successfully")
            else:
                logger.info(f"Notification {pk} was already read")
            return Response({'status': 'Notification marked as read'}, status=status.HTTP_200_OK)
        else:
            logger.warning(
                f"Permission denied - User {request.user.id} tried to mark notification {pk} (recipient: {notification.recipient.id})")
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
