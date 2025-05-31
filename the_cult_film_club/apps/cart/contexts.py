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
    discount_code = request.session.get("discount_code", "")
    discount_percent = request.session.get("discount_percent", 0)
    discount_amount = Decimal('0.00')
    sorting_by_copies = request.GET.get('sort') == 'copies_available'

    # Calculate subtotal
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

    # Calculate delivery based on subtotal (not discounted)
    standard_delivery = (
        subtotal * (Decimal(str(settings.DELIVERY_RATE)) / Decimal('100'))
        if subtotal < settings.FREE_DELIVERY else Decimal('0.00')
    )

    delivery_option = request.session.get('delivery_option', 'standard')
    if delivery_option == 'next_day' and can_next_day:
        delivery = next_day_flat_rate
        free_delivery_diff = 0
    elif subtotal < settings.FREE_DELIVERY:
        delivery = standard_delivery
        free_delivery_diff = settings.FREE_DELIVERY - subtotal
    else:
        delivery = Decimal('0.00')
        free_delivery_diff = 0

    # Calculate discount (on subtotal only)
    if discount_percent:
        discount_amount = subtotal * Decimal(discount_percent) / Decimal('100')
    else:
        discount_amount = Decimal('0.00')

    # Final total: subtotal + delivery - discount
    total = subtotal + delivery - discount_amount

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
        'discount_code': discount_code,
        'discount_percent': discount_percent,
        'discount_amount': discount_amount,
        'sorting_by_copies': sorting_by_copies,
    }
    return context
