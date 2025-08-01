from django.db import models
from django.core.validators import MinValueValidator
from autoslug import AutoSlugField


class Product(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(populate_from='title', unique=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(1)])
    affiliate_url = models.URLField()
    image = models.ImageField(
        upload_to='product_images/', blank=True, null=True)
    category = models.ForeignKey(
        'Category', on_delete=models.PROTECT, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-updated_at']
        verbose_name_plural = 'Products'


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
