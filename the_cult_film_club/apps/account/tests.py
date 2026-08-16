"""
Tests for profiles, addresses and wishlists.

The profile photograph tests matter because #116 changed how deletion works:
it used to erase the Cloudinary asset, and now blanks the column and leaves
the S3 object, since the instance role holds no delete permission.
"""

from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from the_cult_film_club.apps.account.models import (
    Address,
    Profile,
    Wishlist,
    WishlistItem,
)
from the_cult_film_club.apps.releases.models import Releases


def make_user(username="ada", password="pw-for-test"):
    return User.objects.create_user(
        username=username, email=f"{username}@example.com", password=password
    )


class ProfileSignalTests(TestCase):
    def test_a_profile_is_created_with_the_user(self):
        user = make_user()
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_saving_a_user_again_does_not_create_a_second_profile(self):
        user = make_user()
        user.first_name = "Ada"
        user.save()
        self.assertEqual(Profile.objects.filter(user=user).count(), 1)

    def test_a_new_profile_uses_the_placeholder(self):
        user = make_user()
        self.assertEqual(user.profile.photograph.name, "site/placeholder")

    def test_the_placeholder_is_served_from_cloudfront(self):
        user = make_user()
        self.assertTrue(
            user.profile.photograph.url.startswith(
                "https://media.cultfilmclub"
            )
        )

    def test_deleting_a_user_deletes_the_profile(self):
        user = make_user()
        user.delete()
        self.assertEqual(Profile.objects.count(), 0)


class ProfilePhotoTests(TestCase):
    def setUp(self):
        self.user = make_user()
        self.client.login(username="ada", password="pw-for-test")
        self.profile = self.user.profile

    def test_deleting_a_photo_restores_the_placeholder(self):
        self.profile.photograph = "profiles/some_upload"
        self.profile.save()

        self.client.post(reverse("user_profile"), {"delete_photo": "1"})

        self.profile.refresh_from_db()
        self.assertEqual(self.profile.photograph.name, "site/placeholder")

    def test_deleting_when_there_is_no_photo_changes_nothing(self):
        self.client.post(reverse("user_profile"), {"delete_photo": "1"})
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.photograph.name, "site/placeholder")


class AddressTests(TestCase):
    def setUp(self):
        self.user = make_user()

    def make_address(self, label="Home", default=False):
        return Address.objects.create(
            user=self.user,
            first_line="1 Example Street",
            city="London",
            postcode="SW1A 1AA",
            country="GB",
            label=label,
            default_address=default,
        )

    def test_a_second_default_address_unsets_the_first(self):
        first = self.make_address("Home", default=True)
        self.make_address("Work", default=True)

        first.refresh_from_db()
        self.assertFalse(first.default_address)

    def test_only_one_address_is_ever_the_default(self):
        self.make_address("Home", default=True)
        self.make_address("Work", default=True)
        self.make_address("Parents", default=True)
        self.assertEqual(
            Address.objects.filter(
                user=self.user, default_address=True
            ).count(),
            1,
        )

    def test_another_users_default_is_not_affected(self):
        other_user = make_user("grace")
        other = Address.objects.create(
            user=other_user,
            first_line="2 Example Street",
            city="London",
            postcode="SW1A 2AA",
            country="GB",
            label="Home",
            default_address=True,
        )
        self.make_address("Home", default=True)

        other.refresh_from_db()
        self.assertTrue(other.default_address)


class WishlistTests(TestCase):
    def setUp(self):
        self.user = make_user()
        self.release = Releases.objects.create(
            title="Tourist Trap",
            release_date=timezone.now().date(),
            price=Decimal("19.99"),
        )

    def test_an_item_can_be_added_to_a_wishlist(self):
        wishlist = Wishlist.objects.create(user=self.user, name="Mine")
        WishlistItem.objects.create(wishlist=wishlist, title=self.release)
        self.assertEqual(wishlist.wishlistitem_set.count(), 1)

    def test_a_wishlist_defaults_to_medium_priority(self):
        wishlist = Wishlist.objects.create(user=self.user, name="Mine")
        item = WishlistItem.objects.create(
            wishlist=wishlist, title=self.release
        )
        self.assertEqual(item.priority, "Medium")

    def test_deleting_a_wishlist_removes_its_items(self):
        wishlist = Wishlist.objects.create(user=self.user, name="Mine")
        WishlistItem.objects.create(wishlist=wishlist, title=self.release)
        wishlist.delete()
        self.assertEqual(WishlistItem.objects.count(), 0)


class ProfileAccessTests(TestCase):
    def test_the_profile_page_requires_login(self):
        response = self.client.get(reverse("user_profile"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_a_logged_in_user_sees_their_profile(self):
        make_user()
        self.client.login(username="ada", password="pw-for-test")
        self.assertEqual(
            self.client.get(reverse("user_profile")).status_code, 200
        )
