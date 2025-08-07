from django.utils.html import format_html
from django.contrib import admin
from .models import MyUser, UserProfile, Notification


@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'thumbnail', 'email', 'username',
                    'first_name', 'last_name', 'location']
    search_fields = ['email', 'username', 'first_name', 'last_name']

    def thumbnail(self, obj):
        if obj.profile_image:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="width: 60px; height: 60px; object-fit: cover;" /></a>',
                obj.profile_image.url,
                obj.profile_image.url
            )
        return 'No Image Available'

    thumbnail.short_description = 'Image'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user__first_name',
                    'user__last_name',   'location', 'joined']
    search_fields = ['user__email', 'user__username', 'location']
    list_filter = ['joined']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    autocomplete_fields = ['recipient']
    list_display = ['id', 'recipient', 'notification_type',
                    'message', 'is_read', 'created_at']
    list_filter = ['is_read']
