from django.shortcuts import (
    render, redirect, reverse, HttpResponse, get_object_or_404)
from django.contrib import messages
from the_cult_film_club.apps.releases.models import Releases
from django.views.decorators.http import require_POST
from django.conf import settings
from datetime import date
from django.http import JsonResponse
from .forms import OrderForm
from .contexts import purchases
from the_cult_film_club.apps.cart.models import OrderLineItem, Order
import stripe
import json
from the_cult_film_club.apps.account.models import Profile


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


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        cart = request.session.get('cart', {})
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'town_or_city': request.POST['town_or_city'],
            'postcode': request.POST['postcode'],
            'county': request.POST['county'],
            'country': request.POST['country'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            if request.user.is_authenticated:
                try:
                    profile = Profile.objects.get(user=request.user)
                    order.user_profile = profile
                except Profile.DoesNotExist:
                    order.user_profile = None
            order.save()
            for item_id, item_data in cart.items():
                try:
                    release = Releases.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            release=release,
                            quantity=item_data,
                        )
                        order_line_item.save()
                except Releases.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your cart wasn't found in our "
                        "database. Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('cart'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(
                reverse('checkout_success', args=[order.order_number])
            )
        else:
            messages.error(request, 'There was an error with your form. \
                Please check the information you entered.')
    else:
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(
                request,
                ("There's nothing in your cart at the moment")
            )
            return redirect(reverse('releases'))
        current_cart = purchases(request)
        grand_total = current_cart['total']
        stripe_total = round(grand_total * 100)  # Convert to cents for Stripe
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )
        order_form = OrderForm()
    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')
    template = 'cart/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }
    return render(request, template, context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'cart' in request.session:
        del request.session['cart']

    template = 'cart/checkout_success.html'
    context = {
        'order': order,
    }
    return render(request, template, context)
