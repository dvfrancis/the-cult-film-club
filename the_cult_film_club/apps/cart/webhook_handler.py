from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from .models import Order, OrderLineItem
from the_cult_film_club.apps.releases.models import Releases

import stripe
import json
from decimal import Decimal


class StripeWH_Handler:
    """
    Handle Stripe webhooks for order creation, stock management,
    and email confirmation after successful payments
    """

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """
        Sends order confirmation email to the user
        """
        cust_email = order.email
        subject = render_to_string(
            'cart/conf_subject.txt',
            {'order_number': order.order_number}
        ).strip()
        body = render_to_string(
            'cart/conf_body.txt',
            {
                'order': order,
                'order_number': order.order_number,
                'email': settings.DEFAULT_FROM_EMAIL,
            }
        )
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [cust_email])

    def handle_event(self, event):
        """
        Handle any unknown or unhandled webhook events
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        Creates the order, associates it with a profile, updates stock,
        and sends a confirmation email
        """
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.get('bag')
        shipping_details = intent.shipping

        # Retrieve charge for billing details
        charge_id = getattr(intent, "latest_charge", None)
        billing_details = None
        if charge_id:
            try:
                charge = stripe.Charge.retrieve(charge_id)
                billing_details = charge.billing_details
            except stripe.error.StripeError:
                return HttpResponse(
                    content=(
                        f'Webhook received: {event["type"]} | '
                        'ERROR: Failed to retrieve charge for billing details.'
                    ),
                    status=400
                )

        if not billing_details:
            return HttpResponse(
                content=(
                    f'Webhook received: {event["type"]} | '
                    'ERROR: Missing billing details'
                ),
                status=400
            )

        # Clean empty shipping fields
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        # Check if the order already exists (idempotency)
        try:
            order = Order.objects.get(stripe_pid=pid)
            return HttpResponse(
                content=(
                    f'Webhook received: {event["type"]} | '
                    'SUCCESS: Verified order already in database'
                ),
                status=200
            )
        except Order.DoesNotExist:
            pass

        # Try to create a new order
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
                original_bag=bag,
                stripe_pid=pid,
                discount=Decimal(intent.metadata.get('discount', 0) or 0),
                discount_code=intent.metadata.get('discount_code', ''),
            )

            # Associate with user profile if possible
            username = intent.metadata.get('username')
            if username:
                User = get_user_model()
                try:
                    user = User.objects.get(username=username)
                    order.user_profile = user.profile
                    order.save()
                except User.DoesNotExist:
                    pass

            # Create line items
            for item_id, item_data in json.loads(bag).items():
                release = Releases.objects.get(id=item_id)
                quantity = item_data if isinstance(item_data, int) else 1

                OrderLineItem.objects.create(
                    order=order,
                    release=release,
                    quantity=quantity,
                )

                # Reduce available copies
                if release.copies_available is not None:
                    release.copies_available = max(
                        release.copies_available - quantity, 0
                    )
                    release.save()

            # Now update total
            order.update_total()

        except IntegrityError:
            # Race condition: order was created in parallel
            order = Order.objects.get(stripe_pid=pid)
            return HttpResponse(
                content=(
                    f'Webhook received: {event["type"]} | '
                    'SUCCESS: Order already created by another process'
                ),
                status=200
            )
        except Exception as e:
            # Roll back on any error
            if order:
                order.delete()
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | ERROR: {e}',
                status=500
            )

        # Send confirmation email
        self._send_confirmation_email(order)

        # Optional: clear session cart
        if order.user_profile and hasattr(self.request, 'session'):
            self.request.session['cart'] = {}
            self.request.session.modified = True

        return HttpResponse(
            content=(
                f'Webhook received: {event["type"]} | '
                'SUCCESS: Created order in webhook'
            ),
            status=200
        )

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]} (payment failed)',
            status=200
        )
