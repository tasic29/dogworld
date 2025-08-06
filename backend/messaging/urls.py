from rest_framework.routers import DefaultRouter

from .views import MessageViewSet
from core.views import NotificationViewSet

router = DefaultRouter()
router.register('messages', MessageViewSet, basename='message')
router.register('notifications', NotificationViewSet, basename='notification')

urlpatterns = router.urls
