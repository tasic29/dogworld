from rest_framework import serializers
from .models import Blog, Post, Tag, Comment, Rating

from core.serializers import PublicUserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class BlogSerializer(serializers.ModelSerializer):
    author = PublicUserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Blog
        fields = ['id', 'author', 'title', 'content',
                  'image', 'created', 'updated', 'tags']
        read_only_fields = ['id', 'author', 'created', 'updated']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'image', 'caption',
                  'youtube_url', 'created_at', 'tag']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'blog', 'content']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'user', 'blog', 'score']
