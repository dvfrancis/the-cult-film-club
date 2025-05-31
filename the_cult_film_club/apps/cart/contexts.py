from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from the_cult_film_club.apps.releases.models import Releases


def purchases(request):
    purchases = []
    subtotal = Decimal('0.00')
    item_count = 0
    total_quantity = 0
    cart = request.session.get('cart', {})
    next_day_flat_rate = Decimal('7.99')
    can_next_day = request.user.is_authenticated

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
        
    standard_delivery = subtotal * (Decimal(str(settings.DELIVERY_RATE)) / Decimal('100')) \
        if subtotal < settings.FREE_DELIVERY else Decimal('0.00')

    delivery_option = request.session.get('delivery_option', 'standard')
    if delivery_option == 'next_day' and can_next_day:
        delivery = next_day_flat_rate
        free_delivery_diff = 0
    elif subtotal < settings.FREE_DELIVERY:
        delivery = subtotal * (Decimal(str(settings.DELIVERY_RATE)) / Decimal('100'))
        free_delivery_diff = settings.FREE_DELIVERY - subtotal
    else:
        delivery = Decimal('0.00')
        free_delivery_diff = 0

    total = delivery + subtotal

    context = {
        'purchases': purchases,
        'subtotal': subtotal,
        'item_count': item_count,
        'total_quantity': total_quantity,
        'delivery_rate': settings.DELIVERY_RATE,
        'delivery': delivery,
        'free_delivery_diff': free_delivery_diff,
        'free_delivery_threshold': settings.FREE_DELIVERY,
        'total': total,
        'can_next_day': can_next_day,
        'standard_delivery': standard_delivery,
        'next_day_flat_rate': next_day_flat_rate,
        'delivery_option': delivery_option,
    }
    return context
