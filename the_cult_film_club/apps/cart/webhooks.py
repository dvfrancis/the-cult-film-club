from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .webhook_handler import StripeWH_Handler
import stripe


@csrf_exempt
def webhook(request):
    """
    Endpoint for handling Stripe webhooks securely

    Verifies the event signature and delegates to the appropriate handler
    based on the event type
    """
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Retrieve the raw body and Stripe's signature header
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        # Verify and construct the event from payload and signature
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=settings.STRIPE_WH_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(f"Invalid payload: {e}", status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(f"Invalid signature: {e}", status=400)
    except Exception as e:
        # Other unexpected errors
        return HttpResponse(f"Webhook error: {e}", status=400)

    # Initialize handler and define event-to-method mapping
    handler = StripeWH_Handler(request)
    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
        'payment_intent.payment_failed':
            handler.handle_payment_intent_payment_failed,
    }

    # Get the event type and corresponding handler method
    event_type = event.get('type')
    event_handler = event_map.get(event_type, handler.handle_event)

    # Process the event
    return event_handler(event)
