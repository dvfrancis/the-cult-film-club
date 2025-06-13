from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .webhook_handler import StripeWH_Handler
import stripe


@csrf_exempt
def webhook(request):
    """Listen for webhooks from Stripe"""
    stripe.api_key = settings.STRIPE_SECRET_KEY

    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WH_SECRET
        )
    except ValueError as e:
        return HttpResponse(content=f"Invalid payload: {e}", status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(content=f"Invalid signature: {e}", status=400)
    except Exception as e:
        return HttpResponse(content=f"Webhook error: {e}", status=400)

    handler = StripeWH_Handler(request)
    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
        'payment_intent.payment_failed':
            handler.handle_payment_intent_payment_failed,
    }
    event_type = event['type']
    event_handler = event_map.get(event_type, handler.handle_event)
    response = event_handler(event)
    return response
