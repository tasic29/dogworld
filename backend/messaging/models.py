import os
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings

from .validators import validate_file_extension, validate_file_size


class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    content = models.TextField(max_length=1000)
    is_read = models.BooleanField(default=False)
    attachment = models.FileField(
        upload_to='attachments/',
        blank=True,
        null=True,
        validators=[validate_file_extension, validate_file_size]
    )
    is_deleted_by_sender = models.BooleanField(default=False)
    is_deleted_by_receiver = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender.username} to {self.receiver.username}'

    class Meta:
        ordering = ['-sent_at']


class Notification(models.Model):
    NOTIFICATION_TYPE_NEW_MESSAGE = 'message'
    NOTIFICATION_TYPE_NEW_COMMENT = 'comment'
    NOTIFICATION_TYPE_AFFILIATE_CLICKED = 'affiliate_click'

    NOTIFICATION_TYPES = [
        (NOTIFICATION_TYPE_NEW_MESSAGE, 'New Message'),
        (NOTIFICATION_TYPE_NEW_COMMENT, 'New Comment'),
        (NOTIFICATION_TYPE_AFFILIATE_CLICKED, 'Affiliate Link Clicked'),
    ]
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(
        max_length=20, choices=NOTIFICATION_TYPES)
    message = models.TextField(default='')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.get_notification_type_display()} for {self.recipient.username}'

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['content_type', 'object_id']),
        ]
        verbose_name_plural = 'Notifications'
