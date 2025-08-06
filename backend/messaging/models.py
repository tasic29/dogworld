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
