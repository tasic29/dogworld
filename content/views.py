from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from .pagination import DefaultPagination
from .permissions import IsAuthorOrAdminOrReadOnly


from .serializers import BlogSerializer, CommentSerializer, PostSerializer, RatingSerializer, TagSerializer
from .models import Blog, Post, Tag, Comment, Rating


class BlogViewSet(ModelViewSet):
    queryset = Blog.objects.select_related(
        'author').prefetch_related('tags').all()
    serializer_class = BlogSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['created', 'updated']
    search_fields = ['title', 'content']
    ordering_fields = ['id', 'created', 'updated']
    pagination_class = DefaultPagination

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
    pagination_class = DefaultPagination

    def get_queryset(self):
        if self.action in ['list', 'retrieve']:
            return Post.objects.all().select_related('author').prefetch_related('tag')
        if self.request.user.is_staff:
            return Post.objects.all()
        return Post.objects.filter(author=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['author'] = self.request.user
        return context


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

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
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
