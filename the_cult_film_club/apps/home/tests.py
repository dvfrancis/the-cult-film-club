"""
Tests for the landing page and the error handlers.

The error page tests exist because those templates share the base template and
its context processors, so a page nobody looks at until something has already
gone wrong is exactly the page that breaks quietly.
"""

from decimal import Decimal

from django.conf import settings
from django.core.files.storage import default_storage
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from the_cult_film_club.apps.releases.models import Images, Releases


class HomePageTests(TestCase):
    def test_the_home_page_renders(self):
        self.assertEqual(self.client.get(reverse("home")).status_code, 200)

    def test_the_home_page_lists_a_release(self):
        Releases.objects.create(
            title="Tourist Trap",
            release_date=timezone.now().date(),
            price=Decimal("19.99"),
        )
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Tourist Trap")

    def test_the_home_page_renders_with_no_releases_at_all(self):
        self.assertEqual(self.client.get(reverse("home")).status_code, 200)

    def test_release_images_are_served_from_cloudfront(self):
        release = Releases.objects.create(
            title="Tourist Trap",
            release_date=timezone.now().date(),
            price=Decimal("19.99"),
        )
        Images.objects.create(
            title=release, image="releases/hero", is_featured=True
        )
        response = self.client.get(reverse("home"))
        self.assertContains(
            response, "media.cultfilmclub.dominicfrancis.co.uk"
        )

    def test_no_cloudinary_url_survives_anywhere_on_the_page(self):
        """
        Guards the #116 migration against a regression.
        """
        response = self.client.get(reverse("home"))
        self.assertNotContains(response, "res.cloudinary.com")


class MediaUrlTests(TestCase):
    """
    Two settings build image addresses, and nothing makes them agree.

    django-storages applies AWS_LOCATION on its own, so a release cover
    reached the right key throughout issue #140. MEDIA_URL is a plain string
    that nothing applies it to, and the site/ images are pasted into templates
    rather than stored on a model, so they were the only ones that used it.
    They pointed at the bucket root for the length of one deploy and would
    have answered 403 the moment the CloudFront origin moved.
    """

    def test_media_url_carries_the_storage_folder(self):
        if not getattr(settings, "AWS_LOCATION", ""):
            self.skipTest("no folder configured")
        self.assertTrue(
            settings.MEDIA_URL.rstrip("/").endswith(
                "/" + settings.AWS_LOCATION
            ),
            "MEDIA_URL must repeat AWS_LOCATION; storage adds it itself and "
            "template references to site/ do not.",
        )

    def test_the_two_mechanisms_agree_for_one_key(self):
        """
        The same key has to produce the same address either way. A prefix
        check is not enough: the buggy MEDIA_URL was a prefix of the storage
        address, so a startswith assertion passed while the bug was live.
        """
        key = "site/holding_image"
        self.assertEqual(
            default_storage.url(key), settings.MEDIA_URL + key
        )

    def test_the_home_page_banners_point_inside_the_folder(self):
        if not getattr(settings, "AWS_LOCATION", ""):
            self.skipTest("no folder configured")
        response = self.client.get(reverse("home"))
        self.assertContains(
            response, "/%s/site/" % settings.AWS_LOCATION
        )


class ErrorPageTests(TestCase):
    def test_an_unknown_url_returns_a_404(self):
        response = self.client.get("/no-such-page-exists/")
        self.assertEqual(response.status_code, 404)

    def test_the_404_page_renders_rather_than_erroring(self):
        """
        The 404 template extends base.html, so it runs every context
        processor. If one of those raises, the error page cannot render and
        the failure becomes a 500 instead.
        """
        response = self.client.get("/no-such-page-exists/")
        self.assertContains(response, "Cult Film Club", status_code=404)
