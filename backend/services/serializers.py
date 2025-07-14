from rest_framework import serializers

from .models import Service


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'slug', 'service_type', 'description', 'contact_email',
                  'phone_number', 'website_url', 'city', 'image', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']
