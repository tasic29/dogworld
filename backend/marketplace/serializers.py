from rest_framework import serializers
from .models import Product, Category, Tag


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'products_count']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'description', 'price', 'affiliate_url',
                  'image', 'category', 'tags', 'is_active', 'created_at', 'updated_at']
