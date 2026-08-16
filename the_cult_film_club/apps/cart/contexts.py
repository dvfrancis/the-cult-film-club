from decimal import Decimal
from django.conf import settings
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
    #
    # A release can disappear while it is still sitting in someone's session,
    # because deleting one through the admin does not touch anybody's cart.
    # This used to call get_object_or_404 here, which was issue #129: a
    # context processor is not a view, so the Http404 was not turned into a
    # 404 page. It went to handler500, and the 500 template then bound its own
    # context, ran this same processor and raised again. The result was that
    # every page on the site failed for that person, error pages included, and
    # they stayed locked out until their session cookie was cleared.
    #
    # Skipping is enough to keep the site up. The ids are collected rather
    # than removed inside the loop, because mutating the dict being iterated
    # raises.
    missing_item_ids = []

    for item_id, quantity in cart.items():
        release = Releases.objects.filter(pk=item_id).first()
        if release is None:
            missing_item_ids.append(item_id)
            continue
        subtotal += release.price * quantity
        total_quantity += quantity
        purchases_list.append({
            'item_id': item_id,
            'quantity': quantity,
            'release': release,
        })

    # Drop the dead ids so the cart heals itself. Without this the lookup
    # above runs again on every request for the life of the session, and the
    # stale entry would be handed to the checkout as part of the bag.
    if missing_item_ids:
        for item_id in missing_item_ids:
            cart.pop(item_id, None)
        request.session['cart'] = cart
        request.session.modified = True

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
