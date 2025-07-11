# Generated by Django 5.2.3 on 2025-06-23 10:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0008_rename_tag_post_tags'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['created_at'], name='content_pos_created_1233b3_idx'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['author', 'created_at'], name='content_pos_author__4dd08b_idx'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['author'], name='content_pos_author__ebea4c_idx'),
        ),
    ]
