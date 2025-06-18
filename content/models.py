from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Blog(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tag', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Blog'


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts'
    )
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    caption = models.TextField(max_length=1000, blank=True)
    youtube_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tag = models.ManyToManyField('Tag', related_name='posts', blank=True)

    def __str__(self):
        return f"Post by {self.author.username} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"


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

    def __str__(self):
        target = self.blog.title if self.blog else f"Post {self.post.id}"
        return f'Comment by {self.user.username} on {target}'

    class Meta:
        ordering = ['-created']


class Rating(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name='ratings')
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    class Meta:
        # Each user can rate a blog only once
        unique_together = ['user', 'blog']

    def __str__(self):
        return f'{self.user.username} rated {self.blog.title} - {self.score} stars'
