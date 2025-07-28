from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import Comment
from messaging.models import Notification


@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        target = instance.blog or instance.post
        if target and target.author != instance.user:
            Notification.objects.create(
                recipient=target.author,
                notification_type=Notification.NOTIFICATION_TYPE_NEW_COMMENT,
                message=f"{instance.user.username} commented on your {'blog' if instance.blog else 'post'}.",
                content_type=ContentType.objects.get_for_model(Comment),
                object_id=instance.id,
            )
