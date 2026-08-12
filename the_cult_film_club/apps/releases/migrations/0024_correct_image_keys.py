"""
Corrects the keys written by 0023_prefix_image_keys.

That migration assumed the column held a bare Cloudinary public id, because
that is what reading the field through the ORM returned while it was still a
CloudinaryField. It is not what the column held. The raw value was the whole
Cloudinary resource path:

    image/upload/v1748091195/w2friuf7hyw7ajnmnmad.png

By the time 0023 ran, 0022 had already turned the field into a plain
ImageField, which hands back the column untouched, so 0023 prefixed the whole
path and produced keys that exist nowhere:

    releases/image/upload/v1748091195/w2friuf7hyw7ajnmnmad.png

The copy command read the same rows through the CloudinaryField and therefore
wrote the objects under the public id alone, which is the key that is actually
in the bucket:

    releases/w2friuf7hyw7ajnmnmad

So the objects are right and the rows are wrong. This strips the
image/upload/v<version>/ segment and the extension, leaving the prefix and the
public id.
"""

import re

from django.db import migrations

# The prefix is already correct and stays. Only what Cloudinary added around
# the public id comes off.
CLOUDINARY_PATH = re.compile(
    r"^(?P<prefix>releases/)"
    r"image/upload/v\d+/"
    r"(?P<public_id>.+?)"
    r"(?P<extension>\.[A-Za-z0-9]+)?$"
)


def correct_keys(apps, schema_editor):
    Images = apps.get_model("releases", "Images")

    for image in Images.objects.all().iterator():
        value = image.image.name or ""
        match = CLOUDINARY_PATH.match(value)
        if not match:
            # Already correct, or the site/ default. Left alone so a re-run
            # is harmless.
            continue

        corrected = f"{match['prefix']}{match['public_id']}"
        Images.objects.filter(pk=image.pk).update(image=corrected)


def unreversible(apps, schema_editor):
    """
    Deliberately does nothing.

    Reversing would mean putting the Cloudinary version number back, and that
    number is not derivable from anything left in the row. Since the corrected
    key is the one that matches the bucket, going back would only reinstate
    values that point at nothing.
    """


class Migration(migrations.Migration):

    dependencies = [
        ("releases", "0023_prefix_image_keys"),
    ]

    operations = [
        migrations.RunPython(correct_keys, unreversible),
    ]
