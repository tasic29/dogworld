from rest_framework import serializers
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'products_count']


class ProductSerializer(serializers.ModelSerializer):
    # For read operations, return the full category object
    category = CategorySerializer(read_only=True)
    # For write operations, accept category ID
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )

    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'description', 'price', 'affiliate_url',
                  'image', 'category', 'category_id', 'is_active', 'created_at', 'updated_at']
