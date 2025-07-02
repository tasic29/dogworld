from django.contrib import admin

from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'service_type',
                    'city', 'is_active', 'updated_at']
    list_filter = ['name', 'service_type', 'city', 'is_active']
    search_fields = ['name', 'service_type', 'description', 'city']
    readonly_fields = ['updated_at', 'created_at']
    list_per_page = 10
