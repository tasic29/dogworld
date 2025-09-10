from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db import transaction
from .models import Message
from core.models import Notification
from django.contrib.contenttypes.models import ContentType
import logging


User = get_user_model()
logger = logging.getLogger(__name__)


@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    """
    Create notification for new messages with improved efficiency and error handling
    """
    if not created:
        return

    # Skip notifications for self-messages or staff messages
    if instance.sender == instance.receiver or instance.sender.is_staff:
        return

    try:
        # Use atomic transaction to prevent race conditions
        with transaction.atomic():
            sender_name = (
                f"{instance.sender.first_name} {instance.sender.last_name}".strip()
                or instance.sender.username
            )

            # Use select_for_update to prevent race conditions on notification updates
            existing_notification = (
                Notification.objects
                .select_for_update()
                .filter(
                    recipient=instance.receiver,
                    notification_type=Notification.NOTIFICATION_TYPE_NEW_MESSAGE,
                    is_read=False,
                    # Only look for recent notifications (last 24 hours) to avoid
                    # grouping with very old unread notifications
                    created_at__gte=timezone.now() - timezone.timedelta(days=1)
                )
                .first()
            )

            if existing_notification:
                # Increment unread counter safely
                unread_count = existing_notification.extra_data.get(
                    "unread_count", 1)
                existing_notification.extra_data["unread_count"] = unread_count + 1
                existing_notification.message = (
                    f"{sender_name} sent you "
                    f"{existing_notification.extra_data['unread_count']} new messages."
                )
                # Update timestamp to show latest activity
                existing_notification.created_at = timezone.now()
                existing_notification.save(
                    update_fields=["extra_data", "message", "created_at"]
                )
                logger.info(
                    f"Updated notification for user {instance.receiver.id}, "
                    f"total unread: {existing_notification.extra_data['unread_count']}"
                )
            else:
                # Create new notification
                notification = Notification.objects.create(
                    recipient=instance.receiver,
                    notification_type=Notification.NOTIFICATION_TYPE_NEW_MESSAGE,
                    message=f"{sender_name} sent you a new message.",
                    content_object=instance,
                    extra_data={"unread_count": 1,
                                "sender_id": instance.sender.id},
                )
                logger.info(
                    f"Created new message notification {notification.id} "
                    f"for user {instance.receiver.id}"
                )

    except Exception as e:
        logger.error(
            f"Failed to create notification for message {instance.id}: {str(e)}",
            exc_info=True
        )
        # Don't raise the exception to prevent message creation from failing
