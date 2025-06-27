from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from the_cult_film_club.apps.releases.models import Releases


def purchases(request):
    """
    Build a detailed cart context dictionary including
    purchases, subtotal, delivery cost, discounts, and totals.

    Also supports sorting by copies_available via GET param
    'sort=copies_available'.
    """
    cart = request.session.get('cart', {})
    discount_code = request.session.get("discount_code", "")
    discount_percent = request.session.get("discount_percent", 0)

    purchases_list = []
    subtotal = Decimal('0.00')
    total_quantity = 0
    sorting_by_copies = request.GET.get('sort') == 'copies_available'

    # Early return for empty cart with default context values
    if not cart:
        return {
            'purchases': [],
            'subtotal': subtotal,
            'total_quantity': total_quantity,
            'delivery_rate': settings.DELIVERY_RATE,
            'delivery': Decimal('0.00'),
            'free_delivery_diff': settings.FREE_DELIVERY,
            'free_delivery_threshold': settings.FREE_DELIVERY,
            'total': Decimal('0.00'),
            'discount_code': '',
            'discount_percent': 0,
            'discount_amount': Decimal('0.00'),
            'sorting_by_copies': sorting_by_copies,
        }

    # Calculate subtotal and total quantities, collect purchase items
    for item_id, quantity in cart.items():
        release = get_object_or_404(Releases, pk=item_id)
        subtotal += release.price * quantity
        total_quantity += quantity
        purchases_list.append({
            'item_id': item_id,
            'quantity': quantity,
            'release': release,
        })

    # Sort purchases list by copies_available if requested
    if sorting_by_copies:
        purchases_list.sort(
            key=lambda x: x['release'].copies_available,
            reverse=True
        )

    # Calculate delivery fee depending on subtotal and free delivery threshold
    delivery = Decimal('0.00')
    free_delivery_diff = Decimal('0.00')
    if subtotal < settings.FREE_DELIVERY:
        delivery_rate = Decimal(settings.DELIVERY_RATE) / Decimal('100')
        delivery = subtotal * delivery_rate
        free_delivery_diff = settings.FREE_DELIVERY - subtotal

    # Calculate discount amount (only on subtotal)
    discount_amount = Decimal('0.00')
    if discount_percent:
        discount_amount = subtotal * Decimal(discount_percent) / Decimal('100')

    # Calculate final total including delivery and discount
    total = subtotal + delivery - discount_amount

    return {
        'purchases': purchases_list,
        'subtotal': subtotal,
        'total_quantity': total_quantity,
        'delivery_rate': settings.DELIVERY_RATE,
        'delivery': delivery,
        'free_delivery_diff': free_delivery_diff,
        'free_delivery_threshold': settings.FREE_DELIVERY,
        'total': total,
        'discount_code': discount_code,
        'discount_percent': discount_percent,
        'discount_amount': discount_amount,
        'sorting_by_copies': sorting_by_copies,
    }
