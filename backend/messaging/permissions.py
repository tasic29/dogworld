from rest_framework import permissions


class MessagePermission(permissions.BasePermission):
    """
    Custom permission for messages.
    - Users can only see messages they sent or received
    - Users can only delete their own messages (soft delete)
    - Staff can see all messages
    """

    def has_object_permission(self, request, view, obj):
        # Staff can do anything
        if request.user.is_staff:
            return True

        # Users can only access messages they're involved in
        if request.method in permissions.SAFE_METHODS:
            return obj.sender == request.user or obj.receiver == request.user

        # For delete operations, users can soft-delete their own messages
        if request.method == 'DELETE':
            return obj.sender == request.user or obj.receiver == request.user

        # Mark as read - only receiver can do this
        if view.action == 'mark_as_read':
            return obj.receiver == request.user

        return False
