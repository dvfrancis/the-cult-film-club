"""
Tests for the cart: order totals, line items, discount codes and the webhook.

This is the money path, so it is covered first and most thoroughly. Every
figure here is checked against settings.FREE_DELIVERY and DELIVERY_RATE rather
than against a literal, so changing either does not silently invalidate the
tests.
"""

import json
from datetime import timedelta
from decimal import Decimal
from unittest.mock import patch
from uuid import uuid4

import stripe

from django.conf import settings
from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils import timezone

from the_cult_film_club.apps.cart.models import (
    DiscountCode,
    Order,
    OrderLineItem,
)
from the_cult_film_club.apps.cart.webhook_handler import StripeWH_Handler
from the_cult_film_club.apps.releases.models import Releases


def make_release(title="Tourist Trap", price="19.99", copies=5):
    return Releases.objects.create(
        title=title,
        release_date=timezone.now().date(),
        price=Decimal(price),
        copies_available=copies,
    )


def make_order(**kwargs):
    """
    Every order gets its own stripe_pid.

    That field is unique with a default of "", so a second order left without
    one violates the constraint. Only one order can ever exist without a
    payment intent, which is a real property of the model rather than a
    quirk of these tests.
    """
    defaults = {
        "full_name": "Ada Lovelace",
        "email": "ada@example.com",
        "phone_number": "01234567890",
        "country": "GB",
        "postcode": "SW1A 1AA",
        "town_or_city": "London",
        "street_address1": "1 Example Street",
        "stripe_pid": f"pi_test_{uuid4().hex}",
    }
    defaults.update(kwargs)
    return Order.objects.create(**defaults)


class OrderNumberTests(TestCase):
    def test_order_number_is_generated_when_absent(self):
        order = make_order()
        self.assertTrue(order.order_number)
        self.assertEqual(len(order.order_number), 32)

    def test_order_numbers_are_unique(self):
        numbers = {make_order().order_number for _ in range(5)}
        self.assertEqual(len(numbers), 5)

    def test_an_existing_order_number_is_not_regenerated(self):
        order = make_order()
        original = order.order_number
        order.full_name = "Grace Hopper"
        order.save()
        self.assertEqual(order.order_number, original)


class LineItemTests(TestCase):
    def setUp(self):
        self.release = make_release(price="19.99")
        self.order = make_order()

    def test_lineitem_total_is_price_times_quantity(self):
        item = OrderLineItem.objects.create(
            order=self.order, release=self.release, quantity=3
        )
        self.assertEqual(item.lineitem_total, Decimal("59.97"))

    def test_saving_a_lineitem_updates_the_order_subtotal(self):
        OrderLineItem.objects.create(
            order=self.order, release=self.release, quantity=2
        )
        self.order.refresh_from_db()
        self.assertEqual(self.order.subtotal, Decimal("39.98"))

    def test_a_second_lineitem_adds_to_the_subtotal(self):
        other = make_release(title="Onibaba", price="10.00")
        OrderLineItem.objects.create(
            order=self.order, release=self.release, quantity=1
        )
        OrderLineItem.objects.create(
            order=self.order, release=other, quantity=1
        )
        self.order.refresh_from_db()
        self.assertEqual(self.order.subtotal, Decimal("29.99"))


class OrderTotalTests(TestCase):
    """
    Delivery is charged at DELIVERY_RATE percent of the subtotal until the
    subtotal reaches FREE_DELIVERY, at which point it is nothing.
    """

    def setUp(self):
        self.order = make_order()

    def add(self, price, quantity=1):
        release = make_release(title=f"Release {price}", price=price)
        OrderLineItem.objects.create(
            order=self.order, release=release, quantity=quantity
        )
        self.order.refresh_from_db()

    def test_delivery_is_charged_below_the_free_threshold(self):
        self.add("20.00")
        expected = (
            Decimal("20.00") * Decimal(settings.DELIVERY_RATE) / Decimal("100")
        )
        self.assertEqual(self.order.delivery_cost, expected)

    def test_delivery_is_free_at_exactly_the_threshold(self):
        self.add(str(settings.FREE_DELIVERY))
        self.assertEqual(self.order.delivery_cost, Decimal("0.00"))

    def test_delivery_is_free_above_the_threshold(self):
        self.add(str(settings.FREE_DELIVERY + 1))
        self.assertEqual(self.order.delivery_cost, Decimal("0.00"))

    def test_total_is_subtotal_plus_delivery(self):
        self.add("20.00")
        self.assertEqual(
            self.order.total,
            self.order.subtotal + self.order.delivery_cost,
        )

    def test_discount_is_subtracted_from_the_total(self):
        self.add(str(settings.FREE_DELIVERY))
        self.order.discount = Decimal("10.00")
        self.order.update_total()
        self.assertEqual(
            self.order.total,
            Decimal(settings.FREE_DELIVERY) - Decimal("10.00"),
        )

    def test_total_never_goes_negative(self):
        """
        A discount larger than the order should floor at zero rather than
        producing a negative charge.
        """
        self.add("20.00")
        self.order.discount = Decimal("9999.00")
        self.order.update_total()
        self.assertEqual(self.order.total, Decimal("0.00"))

    def test_totals_are_rounded_to_two_places(self):
        self.add("19.99", quantity=3)
        for value in (
            self.order.subtotal,
            self.order.delivery_cost,
            self.order.total,
        ):
            self.assertEqual(value, value.quantize(Decimal("0.01")))

    def test_an_order_with_no_lineitems_has_a_zero_subtotal(self):
        self.order.update_total()
        self.assertEqual(self.order.subtotal, Decimal("0.00"))


class DiscountCodeTests(TestCase):
    def make_code(self, code="CULT10", percent=10, days_from=-1, days_to=1,
                  is_active=True):
        today = timezone.now().date()
        return DiscountCode.objects.create(
            code=code,
            percent=percent,
            valid_from=today + timedelta(days=days_from),
            valid_to=today + timedelta(days=days_to),
            is_active=is_active,
        )

    def test_a_current_active_code_is_valid(self):
        self.assertTrue(self.make_code().is_valid())

    def test_an_inactive_code_is_not_valid(self):
        self.assertFalse(self.make_code(is_active=False).is_valid())

    def test_a_code_that_has_expired_is_not_valid(self):
        self.assertFalse(self.make_code(days_from=-10, days_to=-1).is_valid())

    def test_a_code_that_has_not_started_is_not_valid(self):
        self.assertFalse(self.make_code(days_from=1, days_to=10).is_valid())

    def test_a_code_is_valid_on_its_first_day(self):
        self.assertTrue(self.make_code(days_from=0, days_to=5).is_valid())

    def test_a_code_is_valid_on_its_last_day(self):
        self.assertTrue(self.make_code(days_from=-5, days_to=0).is_valid())


class ApplyDiscountViewTests(TestCase):
    def setUp(self):
        today = timezone.now().date()
        self.code = DiscountCode.objects.create(
            code="CULT10",
            percent=10,
            valid_from=today - timedelta(days=1),
            valid_to=today + timedelta(days=1),
        )
        self.url = reverse("apply_discount")

    def test_a_valid_code_is_stored_in_the_session(self):
        self.client.post(self.url, {"discount_code": "CULT10"})
        self.assertEqual(self.client.session["discount_code"], "CULT10")
        self.assertEqual(self.client.session["discount_percent"], 10)

    def test_a_code_is_matched_case_insensitively(self):
        self.client.post(self.url, {"discount_code": "cult10"})
        self.assertEqual(self.client.session["discount_percent"], 10)

    def test_surrounding_whitespace_is_ignored(self):
        self.client.post(self.url, {"discount_code": "  CULT10  "})
        self.assertEqual(self.client.session["discount_percent"], 10)

    def test_an_unknown_code_clears_the_session(self):
        self.client.post(self.url, {"discount_code": "NOPE"})
        self.assertEqual(self.client.session["discount_code"], "")
        self.assertEqual(self.client.session["discount_percent"], 0)

    def test_an_expired_code_clears_the_session(self):
        today = timezone.now().date()
        DiscountCode.objects.create(
            code="OLD",
            percent=50,
            valid_from=today - timedelta(days=10),
            valid_to=today - timedelta(days=5),
        )
        self.client.post(self.url, {"discount_code": "OLD"})
        self.assertEqual(self.client.session["discount_percent"], 0)

    def test_an_expired_code_replaces_a_previously_applied_one(self):
        """
        The dangerous case: a good code is applied, then a bad one is tried.
        The bad attempt must clear the good discount rather than leave it.
        """
        self.client.post(self.url, {"discount_code": "CULT10"})
        self.client.post(self.url, {"discount_code": "NOPE"})
        self.assertEqual(self.client.session["discount_percent"], 0)

    def test_it_redirects_to_the_cart(self):
        response = self.client.post(self.url, {"discount_code": "CULT10"})
        self.assertRedirects(response, reverse("cart"))


class CartContextTests(TestCase):
    """
    The context processor that every template reads its cart figures from.
    """

    def setUp(self):
        self.release = make_release(price="20.00")

    def set_cart(self, cart, **session):
        s = self.client.session
        s["cart"] = cart
        for key, value in session.items():
            s[key] = value
        s.save()

    def context(self):
        return self.client.get(reverse("cart")).context

    def test_an_empty_cart_reports_zeroes(self):
        context = self.context()
        self.assertEqual(context["subtotal"], Decimal("0.00"))
        self.assertEqual(context["total"], Decimal("0.00"))
        self.assertEqual(context["total_quantity"], 0)
        self.assertEqual(context["purchases"], [])

    def test_an_empty_cart_reports_the_full_free_delivery_gap(self):
        self.assertEqual(
            self.context()["free_delivery_diff"], settings.FREE_DELIVERY
        )

    def test_subtotal_and_quantity_reflect_the_cart(self):
        self.set_cart({str(self.release.id): 2})
        context = self.context()
        self.assertEqual(context["subtotal"], Decimal("40.00"))
        self.assertEqual(context["total_quantity"], 2)

    def test_delivery_is_charged_below_the_threshold(self):
        self.set_cart({str(self.release.id): 1})
        expected = (
            Decimal("20.00") * Decimal(settings.DELIVERY_RATE) / Decimal("100")
        )
        self.assertEqual(self.context()["delivery"], expected)

    def test_delivery_is_free_once_the_threshold_is_reached(self):
        quantity = (settings.FREE_DELIVERY // 20) + 1
        self.set_cart({str(self.release.id): quantity})
        context = self.context()
        self.assertEqual(context["delivery"], Decimal("0.00"))
        self.assertEqual(context["free_delivery_diff"], Decimal("0.00"))

    def test_a_discount_percent_reduces_the_total(self):
        self.set_cart(
            {str(self.release.id): 1},
            discount_code="CULT10",
            discount_percent=10,
        )
        context = self.context()
        self.assertEqual(context["discount_amount"], Decimal("2.00"))
        self.assertEqual(
            context["total"],
            context["subtotal"] + context["delivery"] - Decimal("2.00"),
        )

    def test_a_deleted_release_is_ignored_rather_than_crashing(self):
        self.set_cart({str(self.release.id): 1})
        self.release.delete()
        self.assertEqual(self.client.get(reverse("cart")).status_code, 200)

    def test_the_remaining_items_still_total_correctly(self):
        """
        The dead entry must drop out without taking the rest of the cart
        with it.
        """
        survivor = make_release(title="Onibaba", price="15.00")
        self.set_cart({
            str(self.release.id): 1,
            str(survivor.id): 2,
        })
        self.release.delete()

        context = self.context()
        self.assertEqual(context["subtotal"], Decimal("30.00"))
        self.assertEqual(context["total_quantity"], 2)
        self.assertEqual(len(context["purchases"]), 1)

    def test_a_deleted_release_is_pruned_from_the_session(self):
        """
        Otherwise the lookup runs again on every request for the life of the
        session, and the stale id is handed to the checkout as part of the
        bag.
        """
        self.set_cart({str(self.release.id): 1})
        deleted_id = str(self.release.id)
        self.release.delete()

        self.client.get(reverse("cart"))
        self.assertNotIn(deleted_id, self.client.session.get("cart", {}))

    def test_a_cart_of_only_deleted_releases_reports_as_empty(self):
        self.set_cart({str(self.release.id): 1})
        self.release.delete()

        context = self.context()
        self.assertEqual(context["subtotal"], Decimal("0.00"))
        self.assertEqual(context["total"], Decimal("0.00"))
        self.assertEqual(context["purchases"], [])


class CartViewTests(TestCase):
    def setUp(self):
        self.release = make_release()

    def test_the_cart_page_renders(self):
        self.assertEqual(self.client.get(reverse("cart")).status_code, 200)

    def test_adding_a_release_puts_it_in_the_session(self):
        self.client.post(
            reverse("add_to_cart", args=[self.release.id]),
            {"quantity": 2, "redirect_url": reverse("cart")},
        )
        self.assertEqual(
            self.client.session["cart"].get(str(self.release.id)), 2
        )

    def test_removing_a_release_empties_the_session(self):
        self.client.post(
            reverse("add_to_cart", args=[self.release.id]),
            {"quantity": 1, "redirect_url": reverse("cart")},
        )
        self.client.post(
            reverse("remove_from_cart", args=[self.release.id])
        )
        self.assertNotIn(
            str(self.release.id), self.client.session.get("cart", {})
        )


class DeletedReleaseSiteWideTests(TestCase):
    """
    Issue #129. The context processor runs for every template, so a release
    deleted while in someone's cart took down every page rather than just the
    cart, and the error pages could not render either because they bind the
    same context.
    """

    def setUp(self):
        self.release = make_release()
        session = self.client.session
        session["cart"] = {str(self.release.id): 1}
        session.save()
        self.release.delete()

    def test_the_home_page_still_renders(self):
        self.assertEqual(self.client.get(reverse("home")).status_code, 200)

    def test_the_catalogue_still_renders(self):
        self.assertEqual(self.client.get(reverse("releases")).status_code, 200)

    def test_the_about_page_still_renders(self):
        self.assertEqual(self.client.get(reverse("about")).status_code, 200)

    def test_the_404_page_still_renders(self):
        """
        The one that made this unrecoverable. A broken context processor sent
        the 404 to handler500, whose template bound the same context and
        raised again.
        """
        response = self.client.get("/no-such-page-exists/")
        self.assertEqual(response.status_code, 404)


class CheckoutAccessTests(TestCase):
    def test_checkout_requires_login(self):
        response = self.client.get(reverse("checkout"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_discount_code_management_is_refused_to_ordinary_users(self):
        User.objects.create_user(
            username="member", email="m@example.com", password="pw-for-test"
        )
        self.client.login(username="member", password="pw-for-test")
        response = self.client.get(reverse("discount_codes_management"))
        self.assertNotEqual(response.status_code, 200)


class WebhookTests(TestCase):
    """
    The endpoint is unauthenticated and CSRF-exempt, so the signature check is
    the only thing standing between a stranger and the order handler.
    """

    def test_an_unsigned_request_is_rejected(self):
        response = self.client.post(
            reverse("webhook"),
            data="{}",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_a_forged_signature_is_rejected(self):
        response = self.client.post(
            reverse("webhook"),
            data='{"type": "payment_intent.succeeded"}',
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE="t=1,v1=not-a-real-signature",
        )
        self.assertEqual(response.status_code, 400)

    def test_a_rejected_webhook_creates_no_order(self):
        self.client.post(
            reverse("webhook"),
            data='{"type": "payment_intent.succeeded"}',
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE="t=1,v1=not-a-real-signature",
        )
        self.assertEqual(Order.objects.count(), 0)


class WebhookOrderCreationTests(TestCase):
    """
    Issue #129 in its more expensive form. The payment has already been taken
    by the time this runs, so anything that raises here leaves a customer
    charged with no order recorded, and Stripe retrying into the same failure.

    The handler is called directly rather than through the endpoint, because
    the endpoint verifies a signature that cannot be produced in a test.
    """

    def setUp(self):
        self.release = make_release(price="20.00", copies=5)
        self.handler = StripeWH_Handler(RequestFactory().post("/checkout/wh/"))

    def build_event(self, bag):
        return stripe.Event.construct_from(
            {
                "type": "payment_intent.succeeded",
                "data": {
                    "object": {
                        "id": f"pi_test_{uuid4().hex}",
                        "latest_charge": "ch_test_123",
                        "metadata": {"bag": json.dumps(bag)},
                        "shipping": {
                            "name": "Ada Lovelace",
                            "phone": "01234567890",
                            "address": {
                                "country": "GB",
                                "postal_code": "SW1A 1AA",
                                "city": "London",
                                "line1": "1 Example Street",
                                "line2": "",
                                "state": "",
                            },
                        },
                    }
                },
            },
            "sk_test_key",
        )

    def run_handler(self, bag):
        charge = stripe.Charge.construct_from(
            {"billing_details": {"email": "ada@example.com"}}, "sk_test_key"
        )
        with patch("stripe.Charge.retrieve", return_value=charge):
            return self.handler.handle_payment_intent_succeeded(
                self.build_event(bag)
            )

    def test_a_normal_bag_creates_the_order_and_its_line_item(self):
        response = self.run_handler({str(self.release.id): 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.first().lineitems.count(), 1)

    def test_a_deleted_release_does_not_lose_the_order(self):
        """
        Before the fix this raised Releases.DoesNotExist, which escaped the
        only except clause, returned a 500 to Stripe and recorded nothing.
        """
        deleted_id = self.release.id
        self.release.delete()

        response = self.run_handler({str(deleted_id): 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.count(), 1)

    def test_the_surviving_items_are_still_recorded(self):
        survivor = make_release(title="Onibaba", price="15.00")
        deleted_id = self.release.id
        self.release.delete()

        self.run_handler({str(deleted_id): 1, str(survivor.id): 2})

        order = Order.objects.first()
        self.assertEqual(order.lineitems.count(), 1)
        self.assertEqual(order.subtotal, Decimal("30.00"))

    def test_the_original_bag_still_records_what_was_bought(self):
        """
        The line item is gone but the order keeps the bag it was created
        from, so the missing item is recoverable rather than invisible.
        """
        deleted_id = self.release.id
        self.release.delete()

        self.run_handler({str(deleted_id): 1})
        self.assertIn(str(deleted_id), Order.objects.first().original_bag)
