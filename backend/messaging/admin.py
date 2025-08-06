from django.contrib import admin

from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    def short_content(self, obj):
        return (obj.content[:50] + '...') if len(obj.content) > 50 else obj.content
    short_content.short_description = 'Content'

    autocomplete_fields = ['sender', 'receiver']
    list_display = ['id', 'sender', 'receiver', 'short_content', 'sent_at']
    list_filter = ['is_read', 'sent_at']
    list_select_related = ['sender', 'receiver']
    search_fields = [
        'sender__user__first_name',
        'sender__user__last_name',
        'receiver__user__first_name',
        'receiver__user__last_name',
    ]
