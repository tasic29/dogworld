from django.contrib.contenttypes.models import ContentType
from messaging.models import Notification
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
    total_ratings = serializers.IntegerField(
        source='rating_count', read_only=True)
    average_rating = serializers.FloatField(
        source='avg_rating', read_only=True)
    total_comments = serializers.IntegerField(
        source='comment_count', read_only=True)

    class Meta:
        model = Blog
        fields = ['id', 'author', 'title', 'content',
                  'image', 'created', 'updated', 'tags', 'total_comments', 'total_ratings', 'average_rating']
        read_only_fields = ['id', 'author', 'created', 'updated']


class PostSerializer(serializers.ModelSerializer):
    author = PublicUserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    total_ratings = serializers.ReadOnlyField()
    average_rating = serializers.ReadOnlyField()
    total_comments = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'title',  'image', 'caption',
                  'youtube_url', 'created_at', 'tags', 'total_comments', 'total_ratings', 'average_rating']
        read_only_fields = ['id', 'author', 'created_at']

    def create(self, validated_data):
        author = self.context['author']
        tags = validated_data.pop('tags', [])
        post = Post.objects.create(author=author, **validated_data)
        post.tags.set(tags)
        return post

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if tags is not None:
            instance.tags.set(tags)
        instance.save()
        return instance


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

        comment = Comment.objects.create(**validated_data)

        target = validated_data.get('blog') or validated_data.get('post')

        if target and target.author != author:
            Notification.objects.create(
                recipient=target.author,
                notification_type=Notification.NOTIFICATION_TYPE_NEW_COMMENT,
                message=f"{author.username} commented on your {'blog' if validated_data.get('blog') else 'post'}.",
                content_type=ContentType.objects.get_for_model(Comment),
                object_id=comment.id,
            )

        return comment

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

            if self.instance:
                blog = data.get('blog', self.instance.blog)
                post = data.get('post', self.instance.post)
            else:
                blog = data.get('blog')
                post = data.get('post')

            if not blog and not post:
                raise serializers.ValidationError(
                    "Rating must be linked to either a blog or a post.")
            if blog and post:
                raise serializers.ValidationError(
                    "Rating cannot be linked to both a blog and a post.")

        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return Rating.objects.create(**validated_data)

    class Meta:
        model = Rating
        fields = ['id', 'user', 'blog', 'post', 'blog_id', 'post_id', 'score']
        read_only_fields = ['id', 'user']
