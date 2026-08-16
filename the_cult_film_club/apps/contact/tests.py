"""
Tests for the contact form and the notification it sends.
"""

from django.core import mail
from django.test import TestCase
from django.urls import reverse

from the_cult_film_club.apps.contact.forms import ContactUsForm
from the_cult_film_club.apps.contact.models import ContactUs

VALID = {
    "first_name": "Ada",
    "last_name": "Lovelace",
    "email": "ada@example.com",
    "message": "Do you stock Onibaba on 4K?",
}


class ContactFormTests(TestCase):
    def test_a_complete_submission_is_valid(self):
        self.assertTrue(ContactUsForm(data=VALID).is_valid())

    def test_an_invalid_email_is_rejected(self):
        form = ContactUsForm(data={**VALID, "email": "not-an-address"})
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_every_field_is_required(self):
        form = ContactUsForm(data={})
        self.assertFalse(form.is_valid())
        for field in ("first_name", "last_name", "email", "message"):
            self.assertIn(field, form.errors)


class ContactViewTests(TestCase):
    def setUp(self):
        self.url = reverse("contact_us")

    def test_the_page_renders(self):
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_a_valid_submission_is_stored(self):
        self.client.post(self.url, VALID)
        self.assertEqual(ContactUs.objects.count(), 1)
        self.assertEqual(ContactUs.objects.first().email, VALID["email"])

    def test_an_invalid_submission_is_not_stored(self):
        self.client.post(self.url, {**VALID, "email": "nope"})
        self.assertEqual(ContactUs.objects.count(), 0)

    def test_a_valid_submission_sends_a_notification(self):
        """
        The notification was added because enquiries were otherwise only
        visible by looking in the admin.
        """
        self.client.post(self.url, VALID)
        self.assertEqual(len(mail.outbox), 1)

    def test_the_notification_names_the_sender(self):
        self.client.post(self.url, VALID)
        body = mail.outbox[0].body
        self.assertIn(VALID["email"], body)

    def test_no_notification_is_sent_for_an_invalid_submission(self):
        self.client.post(self.url, {**VALID, "email": "nope"})
        self.assertEqual(len(mail.outbox), 0)
