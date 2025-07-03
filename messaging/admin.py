from django.contrib import admin

from .models import Message, Notification


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    autocomplete_fields = ['sender']
    list_display = ['id', 'sender', 'receiver', 'content', 'sent_at']
    list_select_related = ['sender', 'receiver']
    search_fields = [
        'sender__user__first_name',
        'sender__user__last_name',
        'receiver__user__first_name',
        'receiver__user__last_name',
    ]


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    autocomplete_fields = ['recipient']
    list_display = ['id', 'recipient', 'notification_type',
                    'message', 'is_read', 'created_at']
    list_filter = ['is_read']
