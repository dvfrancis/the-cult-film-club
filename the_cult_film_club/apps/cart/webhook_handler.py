from django.http import HttpResponse
from .models import Order, OrderLineItem
from the_cult_film_club.apps.releases.models import Releases
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
import json
import stripe
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.db import IntegrityError


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
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
            content=(
                f'Unhandled webhook received: {event["type"]}'
            ),
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        shipping_details = intent.shipping

        # Always get the charge using latest_charge
        charge_id = getattr(intent, "latest_charge", None)
        if charge_id:
            charge = stripe.Charge.retrieve(charge_id)
            billing_details = charge.billing_details
        else:
            billing_details = None

        # Clean data in the shipping details
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        if not billing_details:
            return HttpResponse(
                content=(
                    f'Webhook received: {event["type"]} | '
                    'ERROR: Missing billing details'
                ),
                status=400
            )

        # --- Idempotency: Only create order if it doesn't exist ---
        try:
            order = Order.objects.get(stripe_pid=pid)
            # Do NOT send confirmation email again!
            return HttpResponse(
                content=(
                    f'Webhook received: {event["type"]} | '
                    'SUCCESS: Verified order already in database'
                ),
                status=200)
        except Order.DoesNotExist:
            pass

        # Try to create the order, handle race condition with IntegrityError
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
                discount=Decimal(intent.metadata.get('discount', 0)),
                discount_code=intent.metadata.get('discount_code', ''),
            )
            # --- Associate user profile if username is present ---
            username = intent.metadata.get('username')
            if username:
                User = get_user_model()
                try:
                    user = User.objects.get(username=username)
                    profile = user.profile
                    order.user_profile = profile
                    order.save()
                except User.DoesNotExist:
                    pass

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
            order.update_total()
        except IntegrityError:
            # Order was created in the meantime by another webhook attempt
            order = Order.objects.get(stripe_pid=pid)
            # Do NOT send confirmation email again!
            return HttpResponse(
                content=(
                    f'Webhook received: {event["type"]} | '
                    'SUCCESS: Order already created by another process'
                ),
                status=200)
        except Exception as e:
            if order:
                order.delete()
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | ERROR: {e}',
                status=500)

        # Only send confirmation email after order is fully built!
        self._send_confirmation_email(order)

        # --- Step 3: Set a flag to clear the cart (if possible) ---
        if order.user_profile and hasattr(self.request, 'session'):
            self.request.session['cart'] = {}
            self.request.session.modified = True

        return HttpResponse(
            content=(
                f'Webhook received: {event["type"]} | '
                'SUCCESS: Created order in webhook'
            ),
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
