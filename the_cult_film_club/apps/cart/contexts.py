from decimal import Decimal
from django.conf import settings


def purchases(request):

    purchases = []
    subtotal = 0
    item_count = 0

    if subtotal < settings.FREE_DELIVERY:
        delivery = subtotal * Decimal(settings.DELIVERY_RATE / 100)
        free_delivery_diff = settings.FREE_DELIVERY - subtotal
    else:
        delivery = 0
        free_delivery_diff = 0
    total = delivery + subtotal
    context = {
        'purchases': purchases,
        'subtotal': subtotal,
        'item_count': item_count,
        'delivery': delivery,
        'free_delivery_diff': free_delivery_diff,
        'free_delivery_threshold': settings.FREE_DELIVERY,
        'total': total,
    }

    return context
