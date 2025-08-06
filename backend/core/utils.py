from django.contrib.contenttypes.models import ContentType
from core.models import Notification


def create_notification(recipient, notification_type, message, content_object):
    return Notification.objects.create(
        recipient=recipient,
        notification_type=notification_type,
        message=message,
        content_type=ContentType.objects.get_for_model(content_object),
        object_id=content_object.id
    )
