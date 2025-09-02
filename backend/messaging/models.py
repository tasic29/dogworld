from django.db import models
from django.utils import timezone
from django.conf import settings

from .validators import validate_file_extension, validate_file_size


class MessageManager(models.Manager):
    def get_conversation(self, user1, user2):
        """Get all messages between two users"""
        return self.filter(
            models.Q(sender=user1, receiver=user2, is_deleted_by_sender=False) |
            models.Q(sender=user2, receiver=user1,
                     is_deleted_by_receiver=False)
        ).order_by('sent_at')

    def get_user_conversations(self, user):
        """Get all conversations for a user with the latest message"""
        from django.db.models import OuterRef, Subquery, Q

        latest_messages = self.filter(
            Q(sender=user, is_deleted_by_sender=False) |
            Q(receiver=user, is_deleted_by_receiver=False)
        ).filter(
            Q(sender=OuterRef('sender'), receiver=OuterRef('receiver')) |
            Q(sender=OuterRef('receiver'), receiver=OuterRef('sender'))
        ).order_by('-sent_at')

        return self.filter(
            Q(sender=user, is_deleted_by_sender=False) |
            Q(receiver=user, is_deleted_by_receiver=False)
        ).annotate(
            latest_message_id=Subquery(latest_messages.values('id')[:1])
        ).filter(id=OuterRef('latest_message_id')).distinct()


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
    # Track when message was read
    read_at = models.DateTimeField(null=True, blank=True)

    objects = MessageManager()

    def __str__(self):
        return f'Message from {self.sender.username} to {self.receiver.username}'

    def mark_as_read(self):
        """Mark message as read and set read timestamp"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])

    def get_other_participant(self, user):
        """Get the other participant in the conversation"""
        return self.receiver if self.sender == user else self.sender

    @property
    def attachment_url(self):
        """Get attachment URL if exists"""
        if self.attachment:
            return self.attachment.url
        return None

    class Meta:
        ordering = ['-sent_at']
        indexes = [
            models.Index(fields=['sender', 'receiver', '-sent_at']),
            models.Index(fields=['receiver', 'is_read']),
        ]
