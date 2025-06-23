from django.urls import path
from rest_framework_nested import routers
from rest_framework.routers import DefaultRouter
from .views import BlogViewSet, CommentViewSet, PostViewSet, RatingViewSet, TagViewSet


router = routers.DefaultRouter()
router.register('blog', BlogViewSet, basename='blog')
router.register('posts', PostViewSet, basename='post')
router.register('comments', CommentViewSet, basename='comment')
router.register('ratings', RatingViewSet, basename='rating')
router.register('tags', TagViewSet, basename='tag')

blog_router = routers.NestedDefaultRouter(router, 'blog', lookup='blog')
blog_router.register('comments', CommentViewSet, basename='blog-comments')
blog_router.register('ratings', RatingViewSet, basename='blog-ratings')

post_router = routers.NestedDefaultRouter(router, 'posts', lookup='post')
post_router.register('comments', CommentViewSet, basename='post-comments')
post_router.register('ratings', RatingViewSet, basename='post-ratings')

urlpatterns = router.urls + blog_router.urls + post_router.urls
