# Generated by Django 5.2.1 on 2025-05-26 10:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("releases", "0008_releases_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rating",
            name="rating",
            field=models.IntegerField(
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(5),
                ]
            ),
        ),
    ]
