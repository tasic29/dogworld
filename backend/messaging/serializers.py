from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from .models import Message
from core.models import Notification
from core.utils import create_notification
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Message
from core.models import Notification
from core.utils import create_notification

User = get_user_model()


class MessageUserSerializer(serializers.ModelSerializer):
    # Serializer for user info in messages
    full_name = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'profile_image']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username

    def get_profile_image(self, obj):
        request = self.context.get("request")
        if obj.profile_image and hasattr(obj.profile_image, 'url'):
            image_url = obj.profile_image.url
            if request:
                return request.build_absolute_uri(image_url)
            return image_url
        return None


class MessageSerializer(serializers.ModelSerializer):
    sender = MessageUserSerializer(read_only=True)
    receiver = MessageUserSerializer(read_only=True)
    receiver_id = serializers.IntegerField(write_only=True)
    attachment_url = serializers.ReadOnlyField()
    time_ago = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            'id', 'sender', 'receiver', 'receiver_id', 'content',
            'attachment', 'attachment_url', 'is_read', 'sent_at',
            'read_at', 'time_ago'
        ]
        read_only_fields = ['id', 'sender', 'is_read', 'sent_at', 'read_at']

    def get_time_ago(self, obj):
        """Human readable time difference"""
        now = timezone.now()
        diff = now - obj.sent_at

        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "Just now"

    def validate_receiver_id(self, value):
        """Validate receiver exists and is not the sender"""
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("Receiver does not exist.")
        return value

    def validate(self, attrs):
        """Validate sender is not receiver"""
        sender_id = self.context.get('sender_id')
        if sender_id and sender_id == attrs.get('receiver_id'):
            raise serializers.ValidationError(
                "You cannot send a message to yourself."
            )
        return attrs

    def create(self, validated_data):
        sender_id = self.context.get('sender_id')
        if not sender_id:
            raise serializers.ValidationError("Authentication required.")

        receiver_id = validated_data.pop('receiver_id')
        receiver = User.objects.get(id=receiver_id)

        message = Message.objects.create(
            sender_id=sender_id,
            receiver=receiver,
            **validated_data
        )

        # Create notification
        sender_name = (
            f"{message.sender.first_name} {message.sender.last_name}".strip()
            or message.sender.username
        )

        create_notification(
            recipient=receiver,
            notification_type=Notification.NOTIFICATION_TYPE_NEW_MESSAGE,
            message=f'{sender_name} sent you a new message.',
            content_object=message
        )

        return message


class ConversationSerializer(serializers.Serializer):
    """Serializer for conversation summaries"""
    participant = MessageUserSerializer(read_only=True)
    latest_message = MessageSerializer(read_only=True)
    unread_count = serializers.IntegerField(read_only=True)
    last_activity = serializers.DateTimeField(read_only=True)
