from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message
from core.models import Notification
from core.utils import create_notification
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    if not created:
        return

    if instance.sender == instance.receiver or instance.sender.is_staff:
        return

    try:
        sender_name = (
            f"{instance.sender.first_name} {instance.sender.last_name}".strip()
            or instance.sender.username
        )

        create_notification(
            recipient=instance.receiver,
            notification_type=Notification.NOTIFICATION_TYPE_NEW_MESSAGE,
            message=f"{sender_name} sent you a new message.",
            content_object=instance
        )
    except Exception as e:
        logger.error(
            f"Failed to create notification for message {instance.id}: {e}"
        )
