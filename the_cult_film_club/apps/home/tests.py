"""
Tests for the landing page and the error handlers.

The error page tests exist because those templates share the base template and
its context processors, so a page nobody looks at until something has already
gone wrong is exactly the page that breaks quietly.
"""

from decimal import Decimal

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
