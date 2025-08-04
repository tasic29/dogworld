from django_filters.rest_framework import FilterSet, CharFilter
from .models import Product


class ProductFilter(FilterSet):
    category = CharFilter(field_name='category__slug', lookup_expr='iexact')

    class Meta:
        model = Product
        fields = ['category', 'created_at']
