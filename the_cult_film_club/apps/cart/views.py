from django.shortcuts import (
    render, redirect, reverse, HttpResponse, get_object_or_404
)
from django.contrib import messages
from the_cult_film_club.apps.releases.models import Releases
from django.views.decorators.http import require_POST
from django.conf import settings
from datetime import date
from django.http import JsonResponse


def shopping_cart(request):
    """Render the shopping cart page"""
    return render(request, 'cart/cart.html')


def add_to_cart(request, item_id):
    """ Add a quantity of the specified product to the shopping cart """
    release = get_object_or_404(Releases, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})
    if item_id in list(cart.keys()):
        cart[item_id] += quantity
        messages.success(
            request, f'Amended {release.title} quantity to {cart[item_id]}'
        )
    else:
        cart[item_id] = quantity
        messages.success(
            request, f'Added {release.title} to your shopping cart'
        )
    request.session['cart'] = cart
    return redirect(redirect_url)


def amend_cart(request, item_id):
    """ Amend the quantity of the specified product in the shopping cart """
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})
    release = get_object_or_404(Releases, pk=item_id)
    delivery_option = request.POST.get('delivery_option', 'standard')
    request.session['delivery_option'] = delivery_option
    if quantity > 0:
        cart[item_id] = quantity
        messages.success(
            request, f'Amended {release.title} quantity to {cart[item_id]}'
        )
    else:
        cart.pop(item_id)
        messages.success(
            request, f'Removed {release.title} from your shopping cart'
        )
    request.session['cart'] = cart
    return redirect(reverse('cart'))


def remove_from_cart(request, item_id):
    """ Remove the item from the shopping bag """
    try:
        cart = request.session.get('cart', {})
        release = get_object_or_404(Releases, pk=item_id)
        cart.pop(item_id)
        messages.success(
            request, f'Removed {release.title} from your shopping cart'
        )
        request.session['cart'] = cart
        if not cart:
            return JsonResponse({'redirect': '/'})
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)


def apply_discount(request):
    if request.method == "POST":
        code = request.POST.get("discount_code", "").strip().upper()
        discount = None
        today = date.today()
        for d in settings.DISCOUNT_CODES:
            if d["code"] == code and today <= date.fromisoformat(d["expires"]):
                discount = d
                break
        if discount:
            request.session["discount_code"] = code
            request.session["discount_percent"] = discount["percent"]
            messages.success(request, f"Discount code '{code}' applied!")
        else:
            request.session["discount_code"] = ""
            request.session["discount_percent"] = 0
            messages.error(request, "Invalid or expired discount code.")
    return redirect("cart")


@require_POST
def set_delivery_option(request):
    option = request.POST.get('delivery_option', 'standard')
    request.session['delivery_option'] = option
    return redirect('cart')
