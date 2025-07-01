from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from django.db.models import Count
from .models import Product, Category, Tag
from django.utils.html import format_html


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'thumbnail', 'title',
                    'price', 'category_link', 'is_active', 'updated_at']
    list_filter = ['is_active', 'category', 'tags', 'updated_at']
    list_editable = ['title', 'price', 'is_active']
    list_select_related = ['category']
    search_fields = ['title', 'description']
    autocomplete_fields = ['category', 'tags']
    readonly_fields = ['thumbnail']
    list_per_page = 10

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('category').prefetch_related('tags')

    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 60px; height: 60px; object-fit: cover;" />', obj.image.url)
        return 'No Image'
    thumbnail.short_description = 'Image Preview'

    @admin.display(ordering='category__name', description='Category')
    def category_link(self, obj):
        if obj.category:
            url = (
                reverse('admin:marketplace_product_changelist')
                + '?'
                + urlencode({'category__id__exact': str(obj.category.id)})
            )
            return format_html('<a href="{}">{}</a>', url, obj.category.name)
        return '-'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'products_count_link']
    search_fields = ['name']
    list_per_page = 10

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(products_count=Count('product'))

    @admin.display(ordering='products_count', description='Product Count')
    def products_count_link(self, obj):
        url = (
            reverse('admin:marketplace_product_changelist')
            + '?'
            + urlencode({'category__id__exact': str(obj.id)})
        )
        return format_html('<a href="{}">{} Products</a>', url, obj.products_count)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    list_per_page = 10
