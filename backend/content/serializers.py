from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
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
    tag_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    total_ratings = serializers.IntegerField(
        source='rating_count', read_only=True)
    average_rating = serializers.FloatField(
        source='avg_rating', read_only=True)
    total_comments = serializers.IntegerField(
        source='comment_count', read_only=True)

    class Meta:
        model = Blog
        fields = ['id', 'author', 'title', 'content',
                  'image', 'created', 'updated', 'tags', 'tag_ids',
                  'total_comments', 'total_ratings', 'average_rating']
        read_only_fields = ['id', 'author', 'created', 'updated']

    def create(self, validated_data):
        tag_ids = validated_data.pop('tag_ids', [])
        blog = Blog.objects.create(**validated_data)
        if tag_ids:
            blog.tags.set(tag_ids)
        return blog

    def update(self, instance, validated_data):
        tag_ids = validated_data.pop('tag_ids', None)
        blog = super().update(instance, validated_data)
        if tag_ids is not None:
            blog.tags.set(tag_ids)
        return blog


class PostSerializer(serializers.ModelSerializer):
    author = PublicUserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    total_ratings = serializers.IntegerField(
        source='rating_count', read_only=True)
    average_rating = serializers.FloatField(
        source='avg_rating', read_only=True)
    total_comments = serializers.IntegerField(
        source='comment_count', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'image', 'caption',
                  'youtube_url', 'created_at', 'tags', 'tag_ids',
                  'total_comments', 'total_ratings', 'average_rating']
        read_only_fields = ['id', 'author', 'created_at']

    def create(self, validated_data):
        author = self.context['author']
        tag_ids = validated_data.pop('tag_ids', [])

        post = Post.objects.create(author=author, **validated_data)

        if tag_ids:
            post.tags.set(tag_ids)

        return post

    def update(self, instance, validated_data):
        tag_ids = validated_data.pop('tag_ids', None)
        post = super().update(instance, validated_data)
        if tag_ids is not None:
            post.tags.set(tag_ids)
        return post


class CommentSerializer(serializers.ModelSerializer):
    user = PublicUserSerializer(read_only=True)
    post = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(), write_only=True, required=False, allow_null=True
    )
    blog = serializers.PrimaryKeyRelatedField(
        queryset=Blog.objects.all(), write_only=True, required=False, allow_null=True
    )
    post_id = serializers.IntegerField(source='post.id', read_only=True)
    blog_id = serializers.IntegerField(source='blog.id', read_only=True)

    def validate(self, data):

        request = self.context.get('request')
        view = self.context.get('view')

        blog_pk = getattr(view, 'kwargs', {}).get('blog_pk')
        post_pk = getattr(view, 'kwargs', {}).get('post_pk')

        if blog_pk:
            data['blog'] = Blog.objects.get(pk=blog_pk)
            data.pop('post', None)
        elif post_pk:
            data['post'] = Post.objects.get(pk=post_pk)
            data.pop('blog', None)
        else:

            blog = data.get('blog')
            post = data.get('post')

            if not blog and not post:
                raise serializers.ValidationError(
                    "Comment must be linked to either a blog or a post.")
            if blog and post:
                raise serializers.ValidationError(
                    "Comment cannot be linked to both a blog and a post.")
        return data

    def create(self, validated_data):
        author = self.context['user']
        validated_data['user'] = author
        return Comment.objects.create(**validated_data)

    class Meta:
        model = Comment
        fields = [
            'id', 'user', 'blog', 'post', 'blog_id', 'post_id', 'content', 'created'
        ]
        read_only_fields = ['id', 'user', 'created']


class RatingSerializer(serializers.ModelSerializer):
    user = PublicUserSerializer(read_only=True)
    blog = serializers.PrimaryKeyRelatedField(
        queryset=Blog.objects.all(), write_only=True, required=False, allow_null=True
    )
    post = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(), write_only=True, required=False, allow_null=True
    )

    blog_id = serializers.IntegerField(source='blog.id', read_only=True)
    post_id = serializers.IntegerField(source='post.id', read_only=True)

    def validate(self, data):
        user = self.context['request'].user
        view = self.context.get('view')

        blog_pk = getattr(view, 'kwargs', {}).get('blog_pk')
        post_pk = getattr(view, 'kwargs', {}).get('post_pk')

        if blog_pk:
            data['blog'] = get_object_or_404(Blog, pk=blog_pk)
        elif post_pk:
            data['post'] = get_object_or_404(Post, pk=post_pk)

        blog = data.get('blog')
        post = data.get('post')

        if blog and Rating.objects.filter(user=user, blog=blog).exists():
            raise serializers.ValidationError(
                "You have already rated this blog.")
        if post and Rating.objects.filter(user=user, post=post).exists():
            raise serializers.ValidationError(
                "You have already rated this post.")

        if (blog and post) or (not blog and not post):
            raise serializers.ValidationError(
                "Rating must be linked to either a blog or a post, not both or neither."
            )

        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return Rating.objects.create(**validated_data)

    class Meta:
        model = Rating
        fields = ['id', 'user', 'blog', 'post', 'blog_id', 'post_id', 'score']
        read_only_fields = ['id', 'user']
