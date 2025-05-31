from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from the_cult_film_club.apps.releases.models import Releases


def purchases(request):

    purchases = []
    subtotal = 0
    item_count = 0
    total_quantity = 0
    cart = request.session.get('cart', {})

    for item_id, quantity in cart.items():
        release = get_object_or_404(Releases, pk=item_id)
        subtotal += quantity * release.price
        item_count += quantity
        total_quantity += quantity
        purchases.append({
            'item_id': item_id,
            'quantity': quantity,
            'release': release,
        })

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
        'total_quantity': total_quantity,
        'delivery': delivery,
        'free_delivery_diff': free_delivery_diff,
        'free_delivery_threshold': settings.FREE_DELIVERY,
        'total': total,
    }

    return context