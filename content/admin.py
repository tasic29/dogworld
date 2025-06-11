from django.contrib import admin
from .models import Blog, Post


admin.site.register(Post)


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
