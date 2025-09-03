from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status

from .models import Notification, MyUser
from .serializers import NotificationSerializer, PublicUserSerializer


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
        notification = self.get_object()
        if notification.recipient == request.user:
            if not notification.is_read:
                notification.is_read = True
                notification.save()
            return Response({'status': 'Notification marked as read'}, status=status.HTTP_200_OK)
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
