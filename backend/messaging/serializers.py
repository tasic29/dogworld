from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from .models import Message
from core.models import Notification
from core.utils import create_notification


class MessageSerializer(serializers.ModelSerializer):
    sender_id = serializers.IntegerField(read_only=True)
    receiver_id = serializers.IntegerField()
    is_read = serializers.BooleanField(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender_id', 'receiver_id',
                  'content', 'attachment', 'is_read', 'sent_at']

    def create(self, validated_data):
        sender_id = self.context['sender_id']
        receiver_id = validated_data.get('receiver_id')
        if sender_id == receiver_id:
            raise serializers.ValidationError(
                'Message sender and receiver cannot be the same person.')

        message = Message.objects.create(sender_id=sender_id, **validated_data)

        sender_name = f"{message.sender.first_name} {message.sender.last_name}".strip(
        )
        if not sender_name:
            sender_name = message.sender.username

        # create Notification
        create_notification(
            recipient=message.receiver,
            notification_type=Notification.NOTIFICATION_TYPE_NEW_MESSAGE,
            message=f'{sender_name} sent you a new message.',
            content_object=message
        )
        return message
