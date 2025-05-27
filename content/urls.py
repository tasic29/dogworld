from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import BlogViewSet, CommentViewSet, PostViewSet, RatingViewSet, TagViewSet


router = DefaultRouter()
router.register('blog', BlogViewSet, basename='blog')
router.register('post', PostViewSet, basename='post')
router.register('comment', CommentViewSet, basename='comment')
router.register('rating', RatingViewSet, basename='rating')
router.register('tag', TagViewSet, basename='tag')

urlpatterns = router.urls
