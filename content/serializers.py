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
    author = PublicUserSerializer(read_only=True)
    tag = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Post
        fields = ['id', 'author', 'image', 'caption',
                  'youtube_url', 'created_at', 'tag']
        read_only_fields = ['id', 'author', 'created_at']

    def create(self, validated_data):
        author = self.context['author']
        tags = validated_data.pop('tag', [])
        post = Post.objects.create(author=author, **validated_data)
        post.tag.set(tags)
        return post

    def update(self, instance, validated_data):
        tags = validated_data.pop('tag', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if tags is not None:
            instance.tag.set(tags)
        instance.save()
        return instance


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'blog', 'content']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'user', 'blog', 'score']
