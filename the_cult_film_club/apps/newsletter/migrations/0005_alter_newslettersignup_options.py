# Generated by Django 5.2.1 on 2025-06-17 19:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("newsletter", "0004_alter_newslettersignup_unsubscribe_token"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="newslettersignup",
            options={
                "verbose_name": "Subscriber",
                "verbose_name_plural": "Subscribers",
            },
        ),
    ]
