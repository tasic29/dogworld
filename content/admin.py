from django.contrib import admin
from django.db.models import Avg, Count
from django.utils.html import format_html
from .models import Blog, Post, Tag, Comment, Rating


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['id', 'thumbnail', 'title',
                    'created', 'updated']
    autocomplete_fields = ['author']
    search_fields = ['title', 'tag__name']
    ordering = ['-created']
    list_per_page = 10
    list_filter = ['created', 'updated', 'tags']
    list_select_related = ['author']
    list_prefetch_related = ['tags']
    readonly_fields = ['thumbnail']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('author')

    def thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="width: 60px; height: 60px; object-fit: cover;" /></a>',
                obj.image.url,
                obj.image.url
            )
        return 'No Image Available'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'title', 'author', 'caption', 'created_at']
    autocomplete_fields = ['author']
    list_per_page = 10
    list_filter = ['created_at', 'tags']
    search_fields = ['caption', 'tag__name', 'author__username',
                     'author__first_name', 'author__last_name']
    list_select_related = ['author']
    list_per_page = 10

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('author').prefetch_related('tags').annotate(
            avg_rating=Avg('ratings__score'),
            rating_count=Count('ratings', distinct=True),
            comment_count=Count('comments', distinct=True)
        )

    def thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="width: 60px; height: 60px; object-fit: cover;" /></a>',
                obj.image.url,
                obj.image.url
            )
        return 'No Image Available'

    thumbnail.short_description = 'Image'

    def short_caption(self, obj):
        return (obj.caption[:47] + "...") if obj.caption and len(obj.caption) > 50 else obj.caption
    short_caption.short_description = 'Caption'

    def average_rating(self, obj):
        return round(obj.avg_rating or 0, 1)
    average_rating.short_description = 'Avg Rating'

    def rating_count(self, obj):
        return obj.rating_count
    rating_count.short_description = 'Ratings'

    def comment_count(self, obj):
        return obj.comment_count
    comment_count.short_description = 'Comments'

    def thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="width: 60px; height: 60px; object-fit: cover;" /></a>',
                obj.image.url,
                obj.image.url
            )
        return 'No Image Available'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    list_editable = ['name']
    list_per_page = 10


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'blog', 'post', 'short_content', 'created']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    list_filter = ['created', 'blog', 'post']
    list_per_page = 10

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'blog', 'post')

    def short_content(self, obj):
        return (obj.content[:47] + "...") if obj.content and len(obj.content) > 50 else obj.content
    short_content.short_description = 'Content'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'blog', 'post', 'score']
    search_fields = ['user__username', 'user__first_name',
                     'user__last_name', 'blog__title', 'post__title']
    list_filter = ['blog', 'post', 'user']
    list_per_page = 10
