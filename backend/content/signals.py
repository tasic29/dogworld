from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import Comment
from core.models import Notification
from core.utils import create_notification


@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        target = instance.blog or instance.post
        if target and target.author != instance.user:
            create_notification(
                recipient=target.author,
                notification_type='comment',
                message=f"{instance.user.username} commented on your {'blog' if instance.blog else 'post'}.",
                content_object=instance
            )
