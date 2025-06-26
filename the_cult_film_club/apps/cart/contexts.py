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
    discount_code = request.session.get("discount_code", "")
    discount_percent = request.session.get("discount_percent", 0)
    discount_amount = Decimal('0.00')
    sorting_by_copies = request.GET.get('sort') == 'copies_available'

    if not cart:
        context = {
            'purchases': [],
            'subtotal': Decimal('0.00'),
            'item_count': 0,
            'total_quantity': 0,
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
        return context

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

    # Calculate delivery fee based on subtotal and free delivery threshold
    if subtotal < settings.FREE_DELIVERY:
        delivery_rate = Decimal(str(settings.DELIVERY_RATE)) / Decimal('100')
        delivery = subtotal * delivery_rate
        free_delivery_diff = settings.FREE_DELIVERY - subtotal
    else:
        delivery = Decimal('0.00')
        free_delivery_diff = Decimal('0.00')

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
        'discount_code': discount_code,
        'discount_percent': discount_percent,
        'discount_amount': discount_amount,
        'sorting_by_copies': sorting_by_copies,
    }
    return context
