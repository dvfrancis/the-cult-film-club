from django.http import HttpResponse
from .models import Order, OrderLineItem
from the_cult_film_club.apps.releases.models import Releases
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
import json
import time
import stripe


class StripeWH_Handler:
    """Handle Stripe webhooks"""
    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """
        Send confirmation email to the user
        """
        cust_email = order.email
        subject = render_to_string(
            'cart/conf_subject.txt',
            {
                'order_number': order.order_number,
                'email': settings.DEFAULT_FROM_EMAIL
            }
        ).strip()
        body = render_to_string(
            'cart/conf_body.txt',
            {
                'order_number': order.order_number,
                'email': settings.DEFAULT_FROM_EMAIL,
                'order': order,
            }
        )
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )

    def handle_event(self, event):
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        # save_info = intent.metadata.save_info
        shipping_details = intent.shipping

        # Always get the charge using latest_charge
        charge_id = getattr(intent, "latest_charge", None)
        if charge_id:
            charge = stripe.Charge.retrieve(charge_id)
            billing_details = charge.billing_details
            grand_total = round(charge.amount / 100, 2)
        else:
            billing_details = None
            grand_total = round(intent.amount / 100, 2)

        # Clean data in the shipping details
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        order_exists = False
        attempt = 1
        if not billing_details:
            return HttpResponse(
                content=(
                    f'Webhook received: {event["type"]} | '
                    'ERROR: Missing billing details'
                ),
                status=400
            )

        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=billing_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    total=grand_total,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            self._send_confirmation_email(order)
            return HttpResponse(
                content=(
                    f'Webhook received: {event["type"]} | '
                    'SUCCESS: Verified order already in database'
                ),
                status=200)
        else:
            order = None
            try:
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    town_or_city=shipping_details.address.city,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    total=grand_total,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                for item_id, item_data in json.loads(bag).items():
                    release = Releases.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            release=release,
                            quantity=item_data,
                        )
                        order_line_item.save()
                        # --- Update stock ---
                        if release.copies_available is not None:
                            release.copies_available = max(
                                release.copies_available - item_data, 0
                            )
                            release.save()
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)
        self._send_confirmation_email(order)
        return HttpResponse(
            content=(
                f'Webhook received: {event["type"]} | '
                'SUCCESS: Created order in webhook'
            ),
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
