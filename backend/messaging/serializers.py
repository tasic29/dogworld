from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from .models import Message, Notification


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
        Notification.objects.create(
            recipient=message.receiver,
            notification_type=Notification.NOTIFICATION_TYPE_NEW_MESSAGE,
            message=f'{sender_name} sent you a new message.',
            content_type=ContentType.objects.get_for_model(Message),
            object_id=message.id
        )
        return message


# class NotificationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Notification
#         fields = ['id', 'recipient', 'notification_type', 'message', 'is_read']
#         read_only_fields = ['recipient', 'notification_type', 'message']

    # def update(self, instance, validated_data):
    #     user = self.context['request'].user

    #     if instance.recipient != user:
    #         raise serializers.ValidationError(
    #             "You can only mark your own notifications as read.")

    #     if 'is_read' in validated_data:
    #         instance.is_read = validated_data['is_read']
    #         instance.save()
    #     return instance
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
        comment = obj.content_object
        if hasattr(comment, 'blog') and comment.blog:
            return f"/blog/{comment.blog.id}/#comment-{comment.id}"
        elif hasattr(comment, 'post') and comment.post:
            return f"/post/{comment.post.id}/#comment-{comment.id}"
        return "/"
