from django.db.models import Count, Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAdminUser,
                                        AllowAny)
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from core.pagination import DefaultPagination
from .permissions import IsAuthorOrAdminOrReadOnly


from .serializers import (BlogSerializer,
                          CommentSerializer,
                          PostSerializer,
                          RatingSerializer,
                          TagSerializer)
from .models import Blog, Post, Tag, Comment, Rating


class BlogViewSet(ModelViewSet):
    serializer_class = BlogSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['created', 'updated']
    search_fields = ['title', 'content']
    ordering_fields = ['id', 'created', 'updated']
    pagination_class = DefaultPagination

    def get_queryset(self):
        base_queryset = Blog.objects.select_related('author')

        if self.action == 'list':
            return base_queryset.prefetch_related('tags').annotate(
                avg_rating=Avg('ratings__score'),
                rating_count=Count('ratings', distinct=True),
                comment_count=Count('comments', distinct=True)
            ).order_by('-created')

        elif self.action == 'retrieve':
            return base_queryset.prefetch_related(
                'tags',
                'ratings',
                'comments__user'
            )
        return base_queryset.prefetch_related('tags')

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            if not self.request.user.is_staff:
                self.permission_denied(self.request, message="Admins only.")
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['created_at', 'author', 'tags']
    search_fields = ['caption', 'tag__name', 'author__username',
                     'author__first_name', 'author__last_name']
    ordering_fields = ['id', 'title',  'created_at']
    pagination_class = DefaultPagination

    def get_queryset(self):
        base_queryset = Post.objects.select_related('author')

        if self.action == 'list':
            return base_queryset.prefetch_related('tags').annotate(
                avg_rating=Avg('ratings__score'),
                rating_count=Count('ratings', distinct=True),
                comment_count=Count('comments', distinct=True)
            ).order_by('-created_at')

        elif self.action == 'retrieve':
            return base_queryset.prefetch_related(
                'tags',
                'ratings',
                'comments__user'
            )
        return base_queryset.prefetch_related('tags')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['author'] = self.request.user
        return context


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user__username', 'user__first_name',
                        'user__last_name', 'created']
    search_fields = ['user__username', 'user__first_name',
                     'user__last_name', 'content']
    ordering_fields = ['id', 'created']
    pagination_class = DefaultPagination

    def get_queryset(self):
        queryset = Comment.objects.all().select_related('user', 'blog', 'post')

        blog_pk = self.kwargs.get('blog_pk')
        post_pk = self.kwargs.get('post_pk')

        if blog_pk:
            queryset = queryset.filter(blog_id=blog_pk)
        elif post_pk:
            queryset = queryset.filter(post_id=post_pk)

        return queryset

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("You can only edit your own comments.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("You can only delete your own comments.")
        instance.delete()


class RatingViewSet(ModelViewSet):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Rating.objects.all().select_related('user', 'blog', 'post')

        blog_pk = self.kwargs.get('blog_pk')
        post_pk = self.kwargs.get('post_pk')

        if blog_pk:
            get_object_or_404(Blog, pk=blog_pk)
            return queryset.filter(blog_id=blog_pk)
        elif post_pk:
            get_object_or_404(Post, pk=post_pk)
            return queryset.filter(post_id=post_pk)

        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        blog = serializer.validated_data.get('blog')
        post = serializer.validated_data.get('post')

        if (blog and blog.author == user) or (post and post.author == user):
            raise ValidationError("You cannot rate your own blog or post.")

        serializer.save(user=user)

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("You can only update your own ratings.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("You can only delete your own ratings.")
        instance.delete()


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['id', 'name']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]
