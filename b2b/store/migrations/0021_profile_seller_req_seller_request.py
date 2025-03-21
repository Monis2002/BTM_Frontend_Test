# Generated by Django 4.2.16 on 2025-01-12 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0020_alter_productattribute_product"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="seller_req",
            field=models.CharField(
                blank=True,
                choices=[
                    ("pending", "Pending"),
                    ("accept", "Accept"),
                    ("reject", "Reject"),
                ],
                default="pending",
                max_length=10,
                null=True,
            ),
        ),
        migrations.CreateModel(
            name="Seller_request",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "seller_req",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("pending", "Pending"),
                            ("accept", "Accept"),
                            ("reject", "Reject"),
                        ],
                        default="pending",
                        max_length=10,
                        null=True,
                    ),
                ),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="seller_request",
                        to="store.profile",
                    ),
                ),
            ],
        ),
    ]
