# Generated by Django 5.2.1 on 2025-07-10 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("releases", "0020_remove_releases_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="releases",
            name="copies_available",
            field=models.IntegerField(default=1),
        ),
    ]
