"""
Rewrites every stored profile photograph from a Cloudinary public id to an
S3 key.

Part of issue #116, and the counterpart of releases/0023_prefix_image_keys.
See that migration for why a plain string transform is enough. The only
differences here are the prefix and the default.
"""

from django.db import migrations

PREFIX = "profiles/"

OLD_DEFAULT = "placeholder"
NEW_DEFAULT = "site/placeholder"


def add_prefix(apps, schema_editor):
    Profile = apps.get_model("the_cult_film_club_account", "Profile")

    for profile in Profile.objects.all().iterator():
        value = profile.photograph.name or ""

        if not value:
            new = NEW_DEFAULT
        elif value == OLD_DEFAULT:
            new = NEW_DEFAULT
        elif value.startswith(PREFIX) or value.startswith("site/"):
            # Already migrated, so a re-run is harmless.
            continue
        else:
            new = f"{PREFIX}{value}"

        Profile.objects.filter(pk=profile.pk).update(photograph=new)


def strip_prefix(apps, schema_editor):
    Profile = apps.get_model("the_cult_film_club_account", "Profile")

    for profile in Profile.objects.all().iterator():
        value = profile.photograph.name or ""

        if value == NEW_DEFAULT:
            new = OLD_DEFAULT
        elif value.startswith(PREFIX):
            new = value[len(PREFIX):]
        else:
            continue

        Profile.objects.filter(pk=profile.pk).update(photograph=new)


class Migration(migrations.Migration):

    dependencies = [
        ("the_cult_film_club_account", "0015_alter_profile_photograph"),
    ]

    operations = [
        migrations.RunPython(add_prefix, strip_prefix),
    ]
