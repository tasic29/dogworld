from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from .models import MyUser, Notification
from marketplace.models import Product
from services.models import Service


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'email', 'password',
                  'first_name', 'last_name', 'location']


class UserSerializer(BaseUserSerializer):
    # profile_image = serializers.SerializerMethodField()

    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'first_name',
                  'last_name', 'location', 'date_joined', 'is_active', 'is_staff', 'profile_image']

    def get_profile_image(self, obj):
        request = self.context.get("request")
        if obj.profile_image and hasattr(obj.profile_image, 'url'):
            image_url = obj.profile_image.url
            if request:
                return request.build_absolute_uri(image_url)
            return image_url
        return None


class PublicUserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = MyUser
        fields = ['id', 'username', 'email', 'full_name',
                  'location', 'is_active', 'date_joined', 'profile_image']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

    def get_profile_image(self, obj):
        request = self.context.get("request")
        if obj.profile_image and hasattr(obj.profile_image, 'url'):
            image_url = obj.profile_image.url
            if request:
                return request.build_absolute_uri(image_url)
            return image_url
        return None


class NotificationSerializer(serializers.ModelSerializer):
    target_url = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'notification_type', 'message',
            'is_read', 'target_url'
        ]
        read_only_fields = ['recipient', 'notification_type', 'message']

    def get_target_url(self, obj):
        target = obj.content_object
        if hasattr(target, 'blog') and target.blog:
            return f"/blog/{target.blog.id}/#comment-{target.id}"
        elif hasattr(target, 'post') and target.post:
            return f"/post/{target.post.id}/#comment-{target.id}"
        elif isinstance(target, Product):
            return f"/marketplace/product/{target.slug}"
        elif isinstance(target, Service):
            return f"/services/{target.slug}"
        return "/"
