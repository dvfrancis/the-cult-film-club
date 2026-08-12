"""
Copies every image from Cloudinary into the S3 bucket, once, as part of #116.

Run this BEFORE the migration that rewrites the stored values, because it
reads those values in their Cloudinary form. Safe to run again: keys are
derived from the public id rather than generated, so a second run overwrites
rather than duplicating, and the Cloudinary originals are never touched.

Cloudinary delivery URLs are public, so no Cloudinary credentials are needed.
Writing to S3 does need credentials, which on the apps box come from the
instance role once infra/media-permissions.yaml has been applied.
"""

import mimetypes
from urllib.parse import quote

import boto3
import requests
from botocore.exceptions import ClientError
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from the_cult_film_club.apps.account.models import Profile
from the_cult_film_club.apps.releases.models import Images

# Referenced straight from templates rather than stored in a column, so
# nothing in the database points at them and a query cannot find them. Listed
# here by the public id Cloudinary knows them by, without the extension the
# template URLs carry.
SITE_ASSETS = [
    "holding_image",
    "placeholder",
    "TouristTrap_Banner_i6aurl",
    "The_Keep_Banner_resized_llxpbs",
    "Quatermass_Banner_resized_da4wqp",
]

# The two model defaults. Both are decorative and shared, so they belong under
# site/ rather than with the rows that happen to reference them.
DEFAULTS = {"holding_image", "placeholder"}


class Command(BaseCommand):
    help = "Copy images from Cloudinary to S3, preserving the public id"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="List what would be copied without writing anything",
        )
        parser.add_argument(
            "--include-site",
            action="store_true",
            help=(
                "Also copy the decorative site/ assets. Off by default "
                "because the instance role cannot write that prefix, so a "
                "run on the apps box would fail on them. Needs admin "
                "credentials."
            ),
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]

        cloud_name = settings.CLOUDINARY_STORAGE.get("CLOUD_NAME")
        if not cloud_name:
            raise CommandError(
                "CLOUDINARY_CLOUD_NAME is not set, so the source URLs cannot "
                "be built. This command has to run where the Cloudinary "
                "environment is present."
            )

        bucket = settings.AWS_STORAGE_BUCKET_NAME
        if not bucket:
            raise CommandError("AWS_STORAGE_BUCKET_NAME is not set.")

        plan = self.build_plan(include_site=options["include_site"])
        self.stdout.write(f"{len(plan)} images to copy into {bucket}")

        if dry_run:
            for public_id, key in plan:
                self.stdout.write(f"  {public_id} -> {key}")
            return

        client = boto3.client("s3", region_name=settings.AWS_S3_REGION_NAME)
        copied, failed = 0, []

        for public_id, key in plan:
            try:
                body, content_type = self.fetch(cloud_name, public_id)
            except requests.RequestException as exc:
                failed.append((public_id, f"fetch failed: {exc}"))
                continue

            try:
                client.put_object(
                    Bucket=bucket,
                    Key=key,
                    Body=body,
                    # Set explicitly because the keys carry no extension, so
                    # S3 has nothing to infer from. A wrong value here is
                    # invisible until a browser offers a download instead of
                    # showing the image.
                    ContentType=content_type,
                )
            except ClientError as exc:
                failed.append((public_id, f"upload failed: {exc}"))
                continue

            copied += 1
            self.stdout.write(f"  {key}  {content_type}  {len(body)} bytes")

        self.stdout.write(self.style.SUCCESS(f"copied {copied}"))
        if failed:
            self.stdout.write(self.style.ERROR(f"failed {len(failed)}"))
            for public_id, reason in failed:
                self.stdout.write(self.style.ERROR(f"  {public_id}: {reason}"))
            raise CommandError(
                "Some images did not copy. Nothing was deleted."
            )

    def build_plan(self, include_site=False):
        """
        Returns (public_id, s3_key) pairs, deduplicated and in a stable order.

        The key is the prefix plus the public id unchanged. Keeping the id
        exactly as it is means the migration that rewrites the database only
        has to prepend a prefix, with no lookup table passed between the two
        steps.

        The site/ assets are excluded unless asked for. infra/media-
        permissions.yaml grants the instance role releases/ and profiles/
        only, so a run on the apps box gets AccessDenied on every site/ key.
        That is the intended design rather than a gap: those five images are
        decorative and shared, and nothing in the running application should
        be able to replace the holding image. They were uploaded once with
        admin credentials.
        """
        plan = {}

        for value in Images.objects.values_list("image", flat=True):
            public_id = self.public_id(value)
            if not public_id or public_id in DEFAULTS:
                continue
            plan[public_id] = f"releases/{public_id}"

        for value in Profile.objects.values_list("photograph", flat=True):
            public_id = self.public_id(value)
            if not public_id or public_id in DEFAULTS:
                continue
            plan[public_id] = f"profiles/{public_id}"

        if include_site:
            for public_id in SITE_ASSETS:
                plan[public_id] = f"site/{public_id}"

        return sorted(plan.items())

    @staticmethod
    def public_id(value):
        """
        Reduces a stored value to the Cloudinary public id.

        This exists because reading the column gave two different answers
        depending on when you asked, which is what broke the first attempt at
        this migration. While the field was a CloudinaryField the ORM decoded
        the column and handed back the public id; once it became a plain
        ImageField the same read returned the raw stored path:

            image/upload/v1748091195/w2friuf7hyw7ajnmnmad.png

        The data migration was written against the first behaviour and ran
        under the second, so it prefixed the whole path. Taking the last
        segment and dropping the extension gives the same answer under either,
        and also under the corrected keys the rows hold now.
        """
        name = str(value or "")
        if not name:
            return ""

        last_segment = name.rsplit("/", 1)[-1]
        return last_segment.rsplit(".", 1)[0]

    def fetch(self, cloud_name, public_id):
        """
        Pulls the original asset from the Cloudinary delivery URL.

        No version and no extension: that form returns the current asset in
        the format it was uploaded in, which is what should land in S3.
        """
        url = (
            f"https://res.cloudinary.com/{cloud_name}"
            f"/image/upload/{quote(public_id)}"
        )
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")
        # Cloudinary always sends one, but a proxy in between might not, and
        # guessing from the id is useless because it has no extension.
        if not content_type.startswith("image/"):
            guessed, _ = mimetypes.guess_type(f"{public_id}.jpg")
            content_type = guessed or "application/octet-stream"

        return response.content, content_type
