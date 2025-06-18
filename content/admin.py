from django.contrib import admin
from .models import Blog, Post


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'created', 'updated']
    autocomplete_fields = ['author']
    list_per_page = 10
    list_filter = ['created', 'updated']
    list_select_related = ['author']
    list_prefetch_related = ['tags']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('author')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'image', 'caption', 'created_at']
    autocomplete_fields = ['author']
    list_per_page = 10
    list_filter = ['created_at']
    list_select_related = ['author']
    list_prefetch_related = ['tag']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('author')
