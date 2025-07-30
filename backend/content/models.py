from django.db import models

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class BlogManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('author').annotate(
            avg_rating=models.Avg('ratings__score'),
            rating_count=models.Count('ratings', distinct=True),
            comment_count=models.Count('comments', distinct=True)
        )


class Blog(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/',
                              blank=True,
                              null=True,
                              default='blog_images/b_default.webp')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tag', blank=True)

    objects = BlogManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Blog'
        ordering = ['-created']


class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('author').annotate(
            avg_rating=models.Avg('ratings__score'),
            rating_count=models.Count('ratings', distinct=True),
            comment_count=models.Count('comments', distinct=True)
        )


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts'
    )
    title = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to='post_images/',
        blank=True,
        null=True,
        default='post_images/default.webp'
    )
    caption = models.TextField(max_length=1000, blank=True)
    youtube_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', related_name='posts', blank=True)

    objects = PostManager()

    def __str__(self):
        return f"{self.title} by {self.author.username}"

    class Meta:
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['author', 'created_at']),
            models.Index(fields=['author']),
        ]


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    content = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        target = self.blog.title if self.blog else f"Post {self.post.id}"
        return f'Comment by {self.user.username} on {target}'

    class Meta:
        ordering = ['-created']


class Rating(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE,
        related_name='ratings',
        null=True, blank=True
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE,
        related_name='ratings',
        null=True, blank=True
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    class Meta:
        ordering = ['-id']

    def __str__(self):
        if self.blog:
            target = self.blog.title
        elif self.post:
            target = f"Post {self.post.id}"
        else:
            target = "Unknown"
        return f"Rating {self.score} by {self.user.username} on {target}"
