# Generated by Django 4.2.5 on 2025-01-14 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_remove_category_icon_category_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='icon',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
