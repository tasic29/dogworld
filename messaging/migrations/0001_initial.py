# Generated by Django 5.2.3 on 2025-07-03 08:25

import django.db.models.deletion
import messaging.models
from django.conf import settings
from django.db import migrations, models
from ..validators import validate_file_extension, validate_file_size


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=1000)),
                ('is_read', models.BooleanField(default=False)),
                ('attachment', models.FileField(blank=True, null=True,
                 upload_to='attachments/', validators=[validate_file_extension, validate_file_size])),
                ('is_deleted_by_sender', models.BooleanField(default=False)),
                ('is_deleted_by_receiver', models.BooleanField(default=False)),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                 related_name='received_messages', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                 related_name='sent_messages', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-sent_at'],
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(choices=[('message', 'New Message'), (
                    'comment', 'New Comment'), ('affiliate_click', 'Affiliate Link Clicked')], max_length=20)),
                ('message', models.TextField(default='')),
                ('object_id', models.PositiveIntegerField()),
                ('is_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('content_type', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                 related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Notifications',
                'ordering': ['-created_at'],
                'indexes': [models.Index(fields=['recipient', 'is_read'], name='messaging_n_recipie_b24bf9_idx'), models.Index(fields=['content_type', 'object_id'], name='messaging_n_content_b3431b_idx')],
            },
        ),
    ]
