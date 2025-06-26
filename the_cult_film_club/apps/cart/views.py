from django.shortcuts import (
    render, redirect, reverse, HttpResponse, get_object_or_404)
from django.contrib import messages
from the_cult_film_club.apps.releases.models import Releases
from the_cult_film_club.apps.cart.models import DiscountCode
from the_cult_film_club.apps.cart.forms import DiscountCodeForm
from django.views.decorators.http import require_POST, require_GET
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import OrderForm
from .contexts import purchases
from the_cult_film_club.apps.cart.models import Order
import stripe
import json
from the_cult_film_club.apps.account.models import (
    Profile, Address, Wishlist, WishlistItem
)
from decimal import Decimal


def shopping_cart(request):
    """Render the shopping cart page"""
    return render(request, 'cart/cart.html')


def order_detail(request, order_number):
    order = get_object_or_404(
        Order,
        order_number=order_number,
        user_profile__user=request.user
    )
    messages.info(
        request,
        f"Viewing details for successful order #{order.order_number}"
    )
    return render(request, 'cart/order_detail.html', {'order': order})


def add_to_cart(request, item_id):
    """ Add a quantity of the specified product to the shopping cart """
    release = get_object_or_404(Releases, pk=item_id)
    if release.copies_available < 1:
        messages.error(request, "Sorry, this item is out of stock.")
        return redirect(request.POST.get('redirect_url', '/'))
    quantity_str = request.POST.get('quantity')
    try:
        quantity = int(quantity_str)
    except (TypeError, ValueError):
        messages.error(request, "Invalid quantity")
        return redirect(request.POST.get('redirect_url', '/'))
    redirect_url = request.POST.get('redirect_url', '/')
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
    # --- Remove from wishlist if present ---
    if request.user.is_authenticated:
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            WishlistItem.objects.filter(
                wishlist=wishlist, title=release
            ).delete()
        except Wishlist.DoesNotExist:
            pass
    return redirect(redirect_url)


def amend_cart(request, item_id):
    """ Amend the quantity of the specified product in the shopping cart """
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})
    release = get_object_or_404(Releases, pk=item_id)
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


@require_POST
def remove_from_cart(request, item_id):
    """ Remove the item from the shopping bag """
    cart = request.session.get('cart', {})
    release = get_object_or_404(Releases, pk=item_id)
    removed = cart.pop(item_id, None)
    if removed is not None:
        messages.success(
            request, f'Removed {release.title} from your shopping cart'
        )
        request.session['cart'] = cart
        response = {'success': True}
        if not cart:
            response['redirect'] = '/'
        return JsonResponse(response)
    else:
        messages.error(request, 'Item not found in cart')
        return JsonResponse(
            {'success': False, 'error': 'Item not in cart'},
            status=404
        )


def apply_discount(request):
    if request.method == "POST":
        code = request.POST.get("discount_code", "").strip()
        try:
            discount = DiscountCode.objects.get(code__iexact=code)
            if discount.is_valid():
                request.session["discount_code"] = discount.code
                request.session["discount_percent"] = discount.percent
                messages.success(
                    request,
                    f"Discount code '{discount.code}' applied!"
                )
            else:
                request.session["discount_code"] = ""
                request.session["discount_percent"] = 0
                messages.error(request, "Invalid or expired discount code.")
        except DiscountCode.DoesNotExist:
            request.session["discount_code"] = ""
            request.session["discount_percent"] = 0
            messages.error(request, "Invalid or expired discount code.")
    return redirect("cart")


@require_POST
def cache_checkout_data(request):
    try:
        client_secret = request.POST.get('client_secret')
        if not client_secret:
            return HttpResponse("Missing client_secret", status=400)
        pid = client_secret.split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('cart', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user.username,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(
            request,
            'Sorry, your payment cannot be processed. Please try again later.'
        )
        return HttpResponse(content=e, status=400)


@login_required
def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    discount_amount = 0
    discount_code = ""
    cart = request.session.get('cart', {})

    # Handle discount code submission
    if request.method == 'POST':
        # Check for discount code in POST
        code_entered = request.POST.get('discount_code', '').strip()
        if code_entered:
            try:
                discount = DiscountCode.objects.get(code__iexact=code_entered)
                if discount.is_valid():
                    request.session["discount_percent"] = discount.percent
                    request.session["discount_code"] = discount.code
                    messages.success(
                        request,
                        f"Discount code '{discount.code}' applied!"
                    )
                else:
                    request.session["discount_percent"] = 0
                    request.session["discount_code"] = ""
                    messages.error(request, "This discount code is not valid.")
            except DiscountCode.DoesNotExist:
                request.session["discount_percent"] = 0
                request.session["discount_code"] = ""
                messages.error(request, "Discount code not found.")

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

    if not cart:
        messages.error(
            request,
            ("There's nothing in your cart at the moment")
        )
        return redirect(reverse('releases'))

    current_cart = purchases(request)
    subtotal = current_cart['subtotal']
    grand_total = current_cart['total']
    stripe_total = round(grand_total * 100)  # Convert to cents for Stripe
    stripe.api_key = stripe_secret_key
    discount_percent = request.session.get("discount_percent", 0)
    discount_code = request.session.get("discount_code", "")
    discount_amount = 0
    if discount_percent:
        discount_amount = (
            Decimal(discount_percent) / Decimal(100)
        ) * subtotal

    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
        metadata={
            'bag': json.dumps(cart),
            'discount': str(discount_amount),
            'discount_code': discount_code,
        }
    )

    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
            default_address = Address.objects.filter(
                user=request.user,
                default_address=True
            ).first()
            initial_data = {
                'full_name': (
                    request.user.get_full_name() or profile.user.username
                ),
                'email': request.user.email,
                'phone_number': (
                    default_address.phone_number if default_address else ''
                ),
                'street_address1': (
                    default_address.first_line if default_address else ''
                ),
                'street_address2': (
                    default_address.second_line if default_address else ''
                ),
                'town_or_city': (
                    default_address.city if default_address else ''
                ),
                'postcode': (
                    default_address.postcode if default_address else ''
                ),
                'county': default_address.county if default_address else '',
                'country': default_address.country if default_address else '',
            }
        except Profile.DoesNotExist:
            initial_data = {}
    else:
        initial_data = {}

    order_form = OrderForm(initial=initial_data)
    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')
    template = 'cart/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
        'discount_amount': locals().get('discount_amount', 0),
        'discount_code': discount_code,
        'discount_percent': discount_percent,
    }
    return render(request, template, context)


@login_required
def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    order = get_object_or_404(
        Order,
        order_number=order_number,
        user_profile__user=request.user
    )
    messages.success(
        request,
        (
            (
                (
                    f'Order successfully processed! Your order number is '
                    f'{order_number}. A confirmation email will be sent to '
                    f'{order.email}.'
                )
            )
        )
    )
    if 'cart' in request.session:
        del request.session['cart']
    if 'discount_code' in request.session:
        del request.session['discount_code']
    if 'discount_percent' in request.session:
        del request.session['discount_percent']
    return render(request, 'cart/checkout_success.html', {'order': order})


@login_required
def get_latest_order_number(request):
    """
    Return the latest order number for the logged-in user.
    """
    order = (
        Order.objects.filter(user_profile__user=request.user)
        .order_by('-date')
        .first()
    )
    if order:
        return JsonResponse({'order_number': order.order_number})
    return JsonResponse({'order_number': None})


@login_required
@require_GET
def get_order_number_by_pid(request, pid):
    print(f"Received poll for PID: {pid} by user: {request.user}")
    try:
        order = Order.objects.get(
            stripe_pid=pid,
            user_profile__user=request.user
        )
        print(f"Order found: {order.order_number}")
        return JsonResponse({'order_number': order.order_number})
    except Order.DoesNotExist:
        print("Order not found yet.")
        return JsonResponse({'order_number': None})


def discount_codes_management(request):
    discount_codes = DiscountCode.objects.all().order_by('-valid_from')
    if request.method == 'POST':
        form = DiscountCodeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Discount code added successfully")
            return redirect('discount_codes_management')
    else:
        form = DiscountCodeForm()
    return render(request, 'cart/discount_codes.html', {
        'discount_codes': discount_codes,
        'form': form,
    })


def edit_discount_code(request, code_id):
    code = get_object_or_404(DiscountCode, id=code_id)
    if request.method == 'POST':
        form = DiscountCodeForm(request.POST, instance=code)
        if form.is_valid():
            form.save()
            messages.success(request, "Discount code updated successfully")
            return redirect('discount_codes_management')
    else:
        form = DiscountCodeForm(instance=code)
    return render(request, 'cart/edit_discount_code.html', {
        'form': form,
        'code': code,
    })


def delete_discount_code(request, code_id):
    code = get_object_or_404(DiscountCode, id=code_id)
    if request.method == 'POST':
        code.delete()
        messages.success(request, "Discount code deleted successfully")
        return redirect('discount_codes_management')
    return render(request, 'cart/delete_discount_code.html', {
        'code': code,
    })
