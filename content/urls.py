from django.urls import path
from rest_framework_nested import routers
from rest_framework.routers import DefaultRouter
from .views import BlogViewSet, CommentViewSet, PostViewSet, RatingViewSet, TagViewSet


router = routers.DefaultRouter()
router.register('blogs', BlogViewSet, basename='blog')
router.register('posts', PostViewSet, basename='post')
router.register('rating', RatingViewSet, basename='rating')
router.register('tag', TagViewSet, basename='tag')
router.register('comments', CommentViewSet, basename='comment')

blog_router = routers.NestedDefaultRouter(router, 'blogs', lookup='blog')
blog_router.register('comments', CommentViewSet, basename='blog-comment')

post_router = routers.NestedDefaultRouter(router, 'posts', lookup='post')
post_router.register('comments', CommentViewSet, basename='post-comment')

urlpatterns = router.urls + blog_router.urls + post_router.urls
