"""
Tests for newsletter signup, preferences and token-based unsubscribe.

The unsubscribe token is the interesting part: it is the only thing standing
between a stranger and someone else's subscription, since the link carries no
authentication.
"""

from decimal import Decimal
from uuid import uuid4

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from the_cult_film_club.apps.newsletter.forms import NewsletterSignupForm
from the_cult_film_club.apps.newsletter.models import NewsletterSignup
from the_cult_film_club.apps.releases.models import Releases


class SignupModelTests(TestCase):
    def test_each_subscriber_gets_an_unsubscribe_token(self):
        signup = NewsletterSignup.objects.create(email="ada@example.com")
        self.assertIsNotNone(signup.unsubscribe_token)

    def test_tokens_differ_between_subscribers(self):
        a = NewsletterSignup.objects.create(email="a@example.com")
        b = NewsletterSignup.objects.create(email="b@example.com")
        self.assertNotEqual(a.unsubscribe_token, b.unsubscribe_token)

    def test_an_email_can_only_subscribe_once(self):
        from django.db import IntegrityError

        NewsletterSignup.objects.create(email="ada@example.com")
        with self.assertRaises(IntegrityError):
            NewsletterSignup.objects.create(email="ada@example.com")

    def test_subscribers_are_ordered_newest_first(self):
        first = NewsletterSignup.objects.create(email="first@example.com")
        second = NewsletterSignup.objects.create(email="second@example.com")
        self.assertEqual(
            list(NewsletterSignup.objects.all()), [second, first]
        )


class SignupFormTests(TestCase):
    def setUp(self):
        Releases.objects.create(
            title="Tourist Trap",
            release_date=timezone.now().date(),
            price=Decimal("19.99"),
            genre="Horror",
        )

    def test_genre_choices_come_from_the_catalogue(self):
        form = NewsletterSignupForm()
        self.assertIn(("Horror", "Horror"), form.fields["genres"].choices)

    def test_a_signup_with_a_genre_is_valid(self):
        form = NewsletterSignupForm(
            data={"email": "ada@example.com", "genres": ["Horror"]}
        )
        self.assertTrue(form.is_valid())

    def test_genres_are_stored_comma_separated(self):
        Releases.objects.create(
            title="Onibaba",
            release_date=timezone.now().date(),
            price=Decimal("19.99"),
            genre="Drama",
        )
        form = NewsletterSignupForm(
            data={"email": "ada@example.com", "genres": ["Horror", "Drama"]}
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["genres"], "Horror,Drama")

    def test_a_genre_that_is_not_in_the_catalogue_is_rejected(self):
        form = NewsletterSignupForm(
            data={"email": "ada@example.com", "genres": ["Musical"]}
        )
        self.assertFalse(form.is_valid())


class UnsubscribeTests(TestCase):
    def setUp(self):
        self.signup = NewsletterSignup.objects.create(email="ada@example.com")

    def url_for(self, token):
        return reverse("newsletter_unsubscribe", args=[token])

    def test_a_get_shows_a_confirmation_and_removes_nobody(self):
        """
        Worth asserting rather than assuming. An unsubscribe link lands in an
        inbox, where mail clients and scanners fetch URLs on their own, so a
        GET that deleted the record would unsubscribe people who never
        clicked anything.
        """
        response = self.client.get(
            self.url_for(self.signup.unsubscribe_token)
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            NewsletterSignup.objects.filter(email="ada@example.com").exists()
        )

    def test_a_post_with_the_correct_token_unsubscribes(self):
        self.client.post(self.url_for(self.signup.unsubscribe_token))
        self.assertFalse(
            NewsletterSignup.objects.filter(email="ada@example.com").exists()
        )

    def test_an_unknown_token_is_a_404(self):
        """
        The link carries no authentication, so a guessed or stale token must
        not take anyone off the list.
        """
        response = self.client.post(self.url_for(uuid4()))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(
            NewsletterSignup.objects.filter(email="ada@example.com").exists()
        )

    def test_one_persons_token_does_not_unsubscribe_another(self):
        other = NewsletterSignup.objects.create(email="grace@example.com")
        self.client.post(self.url_for(other.unsubscribe_token))
        self.assertTrue(
            NewsletterSignup.objects.filter(email="ada@example.com").exists()
        )
        self.assertFalse(
            NewsletterSignup.objects.filter(email="grace@example.com").exists()
        )


class SignupViewTests(TestCase):
    def setUp(self):
        Releases.objects.create(
            title="Tourist Trap",
            release_date=timezone.now().date(),
            price=Decimal("19.99"),
            genre="Horror",
        )
        self.url = reverse("newsletter_signup")

    def test_the_page_renders(self):
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_a_valid_signup_is_stored(self):
        self.client.post(
            self.url, {"email": "ada@example.com", "genres": ["Horror"]}
        )
        self.assertTrue(
            NewsletterSignup.objects.filter(email="ada@example.com").exists()
        )

    def test_an_invalid_email_is_not_stored(self):
        self.client.post(
            self.url, {"email": "not-an-address", "genres": ["Horror"]}
        )
        self.assertEqual(NewsletterSignup.objects.count(), 0)
