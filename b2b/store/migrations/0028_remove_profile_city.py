# Generated by Django 4.2.5 on 2025-01-18 08:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0027_profile_city1_alter_city_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='city',
        ),
    ]
