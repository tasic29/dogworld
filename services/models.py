from django.db import models
from autoslug import AutoSlugField


class Service(models.Model):
    SERVICE_TYPES = [
        ('vet', 'Veterinarian'),
        ('grooming', 'Grooming'),
        ('walking', 'Dog Walking'),
        ('boarding', 'Boarding / Pet Sitting'),
        ('training', 'Training'),
        ('breeding', 'Breeding'),
        ('nutrition', 'Nutrition / Diet Consultation'),
        ('insurance', 'Pet Insurance'),
        ('photography', 'Pet Photography'),
        ('transport', 'Pet Transport'),
        ('other', 'Other')
    ]

    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    description = models.TextField(blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)
    city = models.CharField(max_length=100)
    image = models.ImageField(
        upload_to='service_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.name
