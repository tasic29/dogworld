from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class MessagePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.sender == request.user or obj.receiver == request.user or request.user.is_staff

        if request.user.is_staff:
            return True

        if hasattr(view, 'action') and view.action == 'mark_as_read':
            return obj.receiver == request.user

        return obj.sender == request.user
