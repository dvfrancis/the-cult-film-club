"""
Rewrites every stored image value from a Cloudinary public id to an S3 key.

Part of issue #116. Cloudinary kept these at the account root with no folder,
so the column held a bare id like `w2friuf7hyw7ajnmnmad`. The bucket puts
uploaded artwork under releases/, which is the prefix the IAM policy in
infra/media-permissions.yaml grants and the prefix the copy wrote to, so every
row needs that segment prepending.

The copy command deliberately left the ids untouched when it wrote to S3,
which is what lets this be a plain string transform with no lookup table
handed between the two steps.
"""

from django.db import migrations

PREFIX = "releases/"

# The model default, which is decorative and shared rather than uploaded, so
# it lives under site/ where the application has no write access.
OLD_DEFAULT = "holding_image"
NEW_DEFAULT = "site/holding_image"


def add_prefix(apps, schema_editor):
    Images = apps.get_model("releases", "Images")

    for image in Images.objects.all().iterator():
        value = image.image.name or ""

        if not value:
            new = NEW_DEFAULT
        elif value == OLD_DEFAULT:
            new = NEW_DEFAULT
        elif value.startswith(PREFIX) or value.startswith("site/"):
            # Already migrated. Makes a re-run harmless rather than doubling
            # the prefix, which matters because a failed deploy is rolled back
            # by restoring code, not by reversing migrations.
            continue
        else:
            new = f"{PREFIX}{value}"

        Images.objects.filter(pk=image.pk).update(image=new)


def strip_prefix(apps, schema_editor):
    Images = apps.get_model("releases", "Images")

    for image in Images.objects.all().iterator():
        value = image.image.name or ""

        if value == NEW_DEFAULT:
            new = OLD_DEFAULT
        elif value.startswith(PREFIX):
            new = value[len(PREFIX):]
        else:
            continue

        Images.objects.filter(pk=image.pk).update(image=new)


class Migration(migrations.Migration):

    dependencies = [
        ("releases", "0022_alter_images_image"),
    ]

    operations = [
        migrations.RunPython(add_prefix, strip_prefix),
    ]
