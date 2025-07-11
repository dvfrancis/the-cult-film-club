# Generated by Django 5.2.1 on 2025-07-01 16:35

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("the_cult_film_club_account", "0012_remove_profile_address"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="wishlist",
            name="unique_user_wishlist",
        ),
        migrations.AddField(
            model_name="wishlist",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="wishlist",
            name="name",
            field=models.CharField(default="My Wishlist", max_length=100),
        ),
    ]
