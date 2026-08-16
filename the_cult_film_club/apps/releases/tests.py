"""
Tests for the catalogue: release views, ratings and featured images.
"""

from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from the_cult_film_club.apps.releases.models import Images, Rating, Releases


def make_release(title="Tourist Trap", price="19.99", copies=5):
    return Releases.objects.create(
        title=title,
        release_date=timezone.now().date(),
        price=Decimal(price),
        copies_available=copies,
    )


class ReleaseViewTests(TestCase):
    def setUp(self):
        self.release = make_release()

    def test_the_catalogue_renders(self):
        self.assertEqual(self.client.get(reverse("releases")).status_code, 200)

    def test_the_catalogue_lists_a_release(self):
        response = self.client.get(reverse("releases"))
        self.assertContains(response, self.release.title)

    def test_a_release_detail_page_renders(self):
        response = self.client.get(
            reverse("release_details", args=[self.release.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.release.title)

    def test_an_unknown_release_is_a_404(self):
        response = self.client.get(reverse("release_details", args=[999999]))
        self.assertEqual(response.status_code, 404)

    def test_product_management_is_refused_to_anonymous_visitors(self):
        response = self.client.get(reverse("product_management"))
        self.assertNotEqual(response.status_code, 200)

    def test_product_management_is_refused_to_ordinary_users(self):
        User.objects.create_user(
            username="member", email="m@example.com", password="pw-for-test"
        )
        self.client.login(username="member", password="pw-for-test")
        response = self.client.get(reverse("product_management"))
        self.assertNotEqual(response.status_code, 200)


class AverageRatingTests(TestCase):
    def setUp(self):
        self.release = make_release()

    def rate(self, username, score):
        user = User.objects.create_user(
            username=username,
            email=f"{username}@example.com",
            password="pw-for-test",
        )
        Rating.objects.create(user=user, title=self.release, rating=score)

    def test_a_release_with_no_ratings_has_no_average(self):
        self.assertIsNone(self.release.average_rating)

    def test_a_single_rating_is_its_own_average(self):
        self.rate("one", 4)
        self.assertEqual(self.release.average_rating, 4)

    def test_the_average_is_the_mean_of_all_ratings(self):
        self.rate("one", 5)
        self.rate("two", 3)
        self.assertEqual(self.release.average_rating, 4)

    def test_ratings_on_another_release_are_not_counted(self):
        other = make_release(title="Onibaba")
        user = User.objects.create_user(
            username="three", email="t@example.com", password="pw-for-test"
        )
        Rating.objects.create(user=user, title=other, rating=1)
        self.rate("four", 5)
        self.assertEqual(self.release.average_rating, 5)

    def test_a_user_can_only_rate_a_release_once(self):
        """
        Enforced by unique_together on the model.
        """
        from django.db import IntegrityError

        user = User.objects.create_user(
            username="dupe", email="d@example.com", password="pw-for-test"
        )
        Rating.objects.create(user=user, title=self.release, rating=3)
        with self.assertRaises(IntegrityError):
            Rating.objects.create(user=user, title=self.release, rating=5)


class FeaturedImageTests(TestCase):
    def setUp(self):
        self.release = make_release()

    def add_image(self, name, featured=False):
        return Images.objects.create(
            title=self.release,
            image=f"releases/{name}",
            is_featured=featured,
        )

    def test_a_release_with_no_images_has_no_featured_image(self):
        self.assertIsNone(self.release.featured_image)

    def test_the_featured_image_is_the_one_marked_featured(self):
        self.add_image("plain")
        featured = self.add_image("hero", featured=True)
        self.assertEqual(self.release.featured_image, featured)

    def test_marking_an_image_featured_unmarks_the_previous_one(self):
        """
        Images.save clears the flag on every other image for the release, so
        a catalogue card can never have two candidates.
        """
        first = self.add_image("first", featured=True)
        self.add_image("second", featured=True)

        first.refresh_from_db()
        self.assertFalse(first.is_featured)
        self.assertEqual(
            Images.objects.filter(
                title=self.release, is_featured=True
            ).count(),
            1,
        )

    def test_featuring_an_image_does_not_affect_another_release(self):
        other = make_release(title="Onibaba")
        other_image = Images.objects.create(
            title=other, image="releases/other", is_featured=True
        )
        self.add_image("mine", featured=True)

        other_image.refresh_from_db()
        self.assertTrue(other_image.is_featured)

    def test_an_image_defaults_to_the_holding_image(self):
        image = Images.objects.create(title=self.release)
        self.assertEqual(image.image.name, "site/holding_image")

    def test_an_image_url_is_served_from_cloudfront(self):
        image = self.add_image("hero")
        self.assertTrue(
            image.image.url.startswith("https://media.cultfilmclub")
        )
