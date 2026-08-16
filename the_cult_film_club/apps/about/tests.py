"""
Tests for the about page.

Static content, so there is little logic to exercise. What is worth asserting
is that the page still renders, since it shares the base template with
everything else and would break with it.
"""

from django.test import TestCase
from django.urls import reverse


class AboutPageTests(TestCase):
    def test_the_about_page_renders(self):
        self.assertEqual(self.client.get(reverse("about")).status_code, 200)

    def test_the_about_page_includes_the_site_name(self):
        response = self.client.get(reverse("about"))
        self.assertContains(response, "Cult Film Club")
