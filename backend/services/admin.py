from django.contrib import admin
from django.utils.html import format_html

from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'thumbnail', 'name', 'service_type',
                    'city', 'is_active', 'updated_at']
    list_filter = ['name', 'service_type', 'city', 'is_active']
    search_fields = ['name', 'service_type', 'description', 'city']
    readonly_fields = ['updated_at', 'created_at']
    list_per_page = 10

    def thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="width: 60px; height: 60px; object-fit: cover;" /></a>',
                obj.image.url,
                obj.image.url
            )
        return 'No Image Available'

    thumbnail.short_description = 'Image'
