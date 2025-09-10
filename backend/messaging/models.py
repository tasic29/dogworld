from django.db import models
from django.utils import timezone
from django.conf import settings
from django.db.models import Q, Max, Count, Case, When, IntegerField


from .validators import validate_file_extension, validate_file_size


class MessageManager(models.Manager):
    def get_conversation(self, user1, user2):
        """Get all messages between two users"""
        return self.select_related('sender', 'receiver').filter(
            Q(sender=user1, receiver=user2, is_deleted_by_sender=False) |
            Q(sender=user2, receiver=user1, is_deleted_by_receiver=False)
        ).order_by('sent_at')

    def get_user_conversations(self, user):
        """Get all conversations for a user with metadata - OPTIMIZED"""
        from django.contrib.auth import get_user_model
        User = get_user_model()

        # Subquery to get the latest message for each conversation
        conversations = (
            self.filter(
                Q(sender=user, is_deleted_by_sender=False) |
                Q(receiver=user, is_deleted_by_receiver=False)
            )
            .annotate(
                # Determine the other participant
                other_user_id=Case(
                    When(sender=user, then='receiver_id'),
                    default='sender_id',
                    output_field=IntegerField(),
                )
            )
            .values('other_user_id')
            .annotate(
                latest_message_id=Max('id'),
                last_activity=Max('sent_at'),
                unread_count=Count(
                    Case(
                        When(
                            receiver=user,
                            is_read=False,
                            is_deleted_by_receiver=False,
                            then=1
                        ),
                        output_field=IntegerField()
                    )
                )
            )
            .order_by('-last_activity')
        )

        return conversations

    def get_conversation_with_user(self, user, other_user_id):
        """Get conversation between user and specific other user"""
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            other_user = User.objects.get(id=other_user_id)
            return self.get_conversation(user, other_user)
        except User.DoesNotExist:
            return self.none()

    def get_unread_count(self, user):
        """Get total unread message count for user"""
        return self.filter(
            receiver=user,
            is_read=False,
            is_deleted_by_receiver=False
        ).count()

    def mark_conversation_as_read(self, user, other_user):
        """Mark all messages from other_user to user as read"""
        from django.utils import timezone

        return self.filter(
            sender=other_user,
            receiver=user,
            is_read=False,
            is_deleted_by_receiver=False
        ).update(
            is_read=True,
            read_at=timezone.now()
        )


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
        models.Index(fields=['receiver', 'is_read', '-sent_at']),
        models.Index(fields=['is_deleted_by_sender',
                     'is_deleted_by_receiver']),
        models.Index(fields=['receiver', 'is_deleted_by_receiver']),
    ]
