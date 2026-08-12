"""
Corrects the keys written by 0016_prefix_photograph_keys.

The counterpart of releases/0024_correct_image_keys, and the same mistake for
the same reason. See that migration for the full explanation. The only
differences are the prefix and the fact that only two rows are affected, the
third already holding the site/placeholder default.
"""

import re

from django.db import migrations

CLOUDINARY_PATH = re.compile(
    r"^(?P<prefix>profiles/)"
    r"image/upload/v\d+/"
    r"(?P<public_id>.+?)"
    r"(?P<extension>\.[A-Za-z0-9]+)?$"
)


def correct_keys(apps, schema_editor):
    Profile = apps.get_model("the_cult_film_club_account", "Profile")

    for profile in Profile.objects.all().iterator():
        value = profile.photograph.name or ""
        match = CLOUDINARY_PATH.match(value)
        if not match:
            continue

        corrected = f"{match['prefix']}{match['public_id']}"
        Profile.objects.filter(pk=profile.pk).update(photograph=corrected)


def unreversible(apps, schema_editor):
    """
    Deliberately does nothing. The Cloudinary version number cannot be
    reconstructed, and the corrected key is the one that matches the bucket.
    """


class Migration(migrations.Migration):

    dependencies = [
        ("the_cult_film_club_account", "0016_prefix_photograph_keys"),
    ]

    operations = [
        migrations.RunPython(correct_keys, unreversible),
    ]
