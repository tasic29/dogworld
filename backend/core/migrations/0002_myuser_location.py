# Generated by Django 5.2.3 on 2025-07-21 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='location',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
