from django.core.management.base import BaseCommand
from faker import Faker
from content.models import Blog
from core.models import MyUser  # adjust based on your author FK
import random

fake = Faker()


class Command(BaseCommand):
    help = 'Seed the Blog model with fake data'

    def handle(self, *args, **kwargs):
        authors = MyUser.objects.filter(is_staff=True)
        if not authors.exists():
            self.stdout.write(self.style.ERROR(
                "No admin users found to assign as authors."))
            return

        for _ in range(10):  # Number of blogs
            Blog.objects.create(
                author=random.choice(authors),
                title=fake.sentence(nb_words=6),
                content=fake.paragraph(nb_sentences=10),
                image='blog_images/default.jpg'  # or leave blank if optional
            )

        self.stdout.write(self.style.SUCCESS("Fake blog posts created."))
