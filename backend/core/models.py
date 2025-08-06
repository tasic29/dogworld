from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=200, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True, max_length=500)
    location = models.CharField(max_length=100, blank=True)
    favorite_breeds = models.CharField(max_length=255, blank=True)
    joined = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0.0)  # average from reviews

    def __str__(self):
        return f"{self.user.username}'s profile"

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'


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
