# Generated by Django 5.2.1 on 2025-06-09 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0004_order_user_profile"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="discount",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]
