# Generated by Django 5.2.3 on 2025-07-30 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0017_alter_post_image'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together=set(),
        ),
    ]
