# Generated by Django 5.2.1 on 2025-05-18 17:02

import cloudinary.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Images",
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
                    "image",
                    cloudinary.models.CloudinaryField(
                        blank=True,
                        default="placeholder",
                        max_length=255,
                        verbose_name="image",
                    ),
                ),
                ("caption", models.CharField(blank=True, max_length=200)),
                ("date_added", models.DateTimeField(auto_now_add=True)),
                ("is_featured", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Releases",
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
                ("title", models.CharField(max_length=100)),
                ("release_date", models.DateField()),
                (
                    "description",
                    models.TextField(blank=True, max_length=1000, null=True),
                ),
                ("genre", models.CharField(blank=True, max_length=50, null=True)),
                ("subgenre", models.CharField(blank=True, max_length=50, null=True)),
                ("resolution", models.CharField(blank=True, max_length=5, null=True)),
                (
                    "special_features",
                    models.TextField(blank=True, max_length=2000, null=True),
                ),
                ("edition", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "censor_status",
                    models.CharField(blank=True, max_length=10, null=True),
                ),
                ("copies_available", models.IntegerField(blank=True, null=True)),
                ("packaging", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="releases",
                        to="releases.images",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Rating",
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
                ("rating", models.IntegerField()),
                ("review", models.TextField(blank=True, max_length=1500, null=True)),
                ("date_added", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rating",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "title",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ratings",
                        to="releases.releases",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="images",
            name="title",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="images",
                to="releases.releases",
            ),
        ),
    ]
