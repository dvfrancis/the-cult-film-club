from django.shortcuts import (
    render, redirect, reverse, HttpResponse, get_object_or_404
)
from django.contrib import messages
from django.views.decorators.http import require_POST, require_GET
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from decimal import Decimal
import json
import stripe
from the_cult_film_club.apps.releases.models import Releases
from the_cult_film_club.apps.cart.models import DiscountCode, Order
from the_cult_film_club.apps.cart.forms import DiscountCodeForm, OrderForm
from the_cult_film_club.apps.account.models import (
    Profile, Address, Wishlist, WishlistItem
)
from .contexts import purchases
from functools import wraps
from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import redirect_to_login


def superuser_required(view_func):
    """
    Decorator for views that ensures the user is both authenticated and a
    superuser.

    - If the user is not authenticated, redirects them to the login page.
    - If the user is authenticated but not a superuser, raises a
      PermissionDenied (403) error.
    - If the user is a superuser, proceeds to the view as normal.

    Example usage:
        @superuser_required
        def my_view(request):
            ...

    Returns:
        function: Wrapped view with access control applied.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        if not request.user.is_superuser:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def shopping_cart(request):
    """
    Render the shopping cart page.
    """
    return render(request, 'cart/cart.html')


def order_detail(request, order_number):
    """
    Display details of a successful order for the logged-in user.

    Args:
        request: HttpRequest object.
        order_number: The unique order number to look up.

    Returns:
        Rendered order_detail page or 404 if order not found.
    """
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
    """
    Add a quantity of a product to the shopping cart stored in session.
    Also removes the product from the user's wishlist if present.

    Args:
        request: HttpRequest object (expects POST).
        item_id: ID of the product to add.

    Returns:
        Redirect to URL specified by 'redirect_url' POST parameter or '/'.
    """
    release = get_object_or_404(Releases, pk=item_id)

    # Check stock availability
    if release.copies_available < 1:
        messages.error(request, "Sorry, this item is out of stock.")
        return redirect(request.POST.get('redirect_url', '/'))

    # Validate quantity input
    try:
        quantity = int(request.POST.get('quantity'))
    except (TypeError, ValueError):
        messages.error(request, "Invalid quantity")
        return redirect(request.POST.get('redirect_url', '/'))

    redirect_url = request.POST.get('redirect_url', '/')
    cart = request.session.get('cart', {})

    item_key = str(item_id)
    if item_key in cart:
        cart[item_key] += quantity
        messages.success(
            request,
            f'Amended "{release.title}" quantity to {cart[item_key]}'
        )
    else:
        cart[item_key] = quantity
        messages.success(
            request,
            f'Added "{release.title}" to your shopping cart'
        )

    request.session['cart'] = cart

    # Remove from wishlist if user is authenticated
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
    """
    Change the quantity of an existing cart item or remove it if quantity <= 0.

    Args:
        request: HttpRequest object (expects POST).
        item_id: ID of the product to amend.

    Returns:
        Redirects to the cart page.
    """
    try:
        quantity = int(request.POST.get('quantity'))
    except (TypeError, ValueError):
        messages.error(request, "Invalid quantity")
        return redirect(reverse('cart'))

    cart = request.session.get('cart', {})
    release = get_object_or_404(Releases, pk=item_id)
    item_key = str(item_id)

    if quantity > 0:
        cart[item_key] = quantity
        messages.success(
            request,
            f'Amended "{release.title}" quantity to {quantity}'
        )
    else:
        if item_key in cart:
            cart.pop(item_key)
            messages.success(
                request,
                f'Removed "{release.title}" from your shopping cart'
            )

    request.session['cart'] = cart
    return redirect(reverse('cart'))


@require_POST
def remove_from_cart(request, item_id):
    """
    Remove an item entirely from the shopping cart.

    Args:
        request: HttpRequest object (POST only).
        item_id: ID of the product to remove.

    Returns:
        JsonResponse indicating success or failure.
    """
    cart = request.session.get('cart', {})
    release = get_object_or_404(Releases, pk=item_id)
    item_key = str(item_id)

    removed = cart.pop(item_key, None)
    if removed is not None:
        messages.success(
            request,
            f'Removed "{release.title}" from your shopping cart'
        )
        request.session['cart'] = cart
        response = {'success': True}
        # Redirect if cart is empty after removal
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
    """
    Apply a discount code to the current session.

    Expects POST with 'discount_code' in form data.
    Stores valid discount info in session, otherwise clears discount session
    data.

    Returns:
        Redirect to cart page.
    """
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
    """
    Cache checkout metadata in Stripe PaymentIntent before payment
    confirmation.

    Expects 'client_secret' and optional 'save_info' in POST data.

    Returns:
        HttpResponse 200 on success or 400 on failure.
    """
    try:
        client_secret = request.POST.get('client_secret')
        if not client_secret:
            return HttpResponse("Missing client_secret", status=400)

        pid = client_secret.split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('cart', {})),
            'save_info': request.POST.get('save_info', ''),
            'username': (
                request.user.username
                if request.user.is_authenticated else ''
            ),
        })
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(
            request,
            ('Sorry, your payment cannot be processed. '
             'Please try again later.')
        )
        return HttpResponse(content=str(e), status=400)


@login_required
def checkout(request):
    """
    Display and handle the checkout form, process discounts, and create
    Stripe PaymentIntent.

    Supports discount code application via POST.
    Pre-fills user data if authenticated.

    Returns:
        Rendered checkout page or redirects on empty cart.
    """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    cart = request.session.get('cart', {})

    if not cart:
        messages.error(request, "There's nothing in your cart at the moment")
        return redirect(reverse('releases'))

    # Process discount code if submitted via POST
    if request.method == 'POST':
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

        # Prepare form data from POST
        form_data = {
            'full_name': request.POST.get('full_name', ''),
            'email': request.POST.get('email', ''),
            'phone_number': request.POST.get('phone_number', ''),
            'street_address1': request.POST.get('street_address1', ''),
            'street_address2': request.POST.get('street_address2', ''),
            'town_or_city': request.POST.get('town_or_city', ''),
            'postcode': request.POST.get('postcode', ''),
            'county': request.POST.get('county', ''),
            'country': request.POST.get('country', ''),
        }
        order_form = OrderForm(form_data)
    else:
        order_form = None

    discount_percent = request.session.get("discount_percent", 0)
    discount_code = request.session.get("discount_code", "")

    current_cart = purchases(request)
    subtotal = current_cart['subtotal']
    grand_total = current_cart['total']

    # Calculate discount amount
    discount_amount = (
        (Decimal(discount_percent) / Decimal(100)) * subtotal
        if discount_percent else Decimal(0)
    )

    stripe_total = round(grand_total * 100)  # Convert to cents for Stripe

    stripe.api_key = stripe_secret_key

    # Create Stripe PaymentIntent with metadata
    try:
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                'bag': json.dumps(cart),
                'discount': str(discount_amount),
                'discount_code': discount_code,
            }
        )
    except stripe.error.CardError as e:
        messages.error(
            request,
            e.user_message or (
                "Your card was declined. Please try another payment method."
            )
        )
        return redirect(reverse('cart'))

    except stripe.error.RateLimitError:
        messages.error(
            request,
            (
                "Too many payment attempts in a short time. "
                "Please wait and try again."
            )
        )
        return redirect(reverse('cart'))

    except stripe.error.InvalidRequestError as e:
        error_message = str(e)
        if (
            "payment_method_data[billing_details][address][country]"
            in error_message
        ):
            user_msg = (
                "Please ensure you've selected a valid country "
                "in your billing address."
            )
        else:
            user_msg = (
                "There was a problem with your payment request. "
                "Please double-check your details and try again."
            )
        messages.error(request, user_msg)
        return redirect(reverse('cart'))

    except stripe.error.AuthenticationError:
        messages.error(
            request,
            "Payment authentication failed. Please try again later."
        )
        return redirect(reverse('cart'))

    except stripe.error.APIConnectionError:
        messages.error(
            request,
            (
                "Network error. Please check your internet connection "
                "and try again."
            )
        )
        return redirect(reverse('cart'))

    except stripe.error.StripeError:
        messages.error(
            request,
            (
                "Payment failed due to a technical error. "
                "Please try again or contact support."
            )
        )
        return redirect(reverse('cart'))

    except Exception:
        messages.error(
            request,
            "An unexpected error occurred. Please try again."
        )
        return redirect(reverse('cart'))

    # Prepare initial form data for authenticated users
    if not order_form:
        initial_data = {}
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
                    'county': (
                        default_address.county if default_address else ''
                    ),
                    'country': (
                        default_address.country if default_address else ''
                    ),
                }
            except Profile.DoesNotExist:
                pass
        order_form = OrderForm(initial=initial_data)

    if not stripe_public_key:
        messages.warning(
            request,
            (
                'Stripe public key is missing. '
                'Did you forget to set it in your environment?'
            )
        )

    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
        'discount_amount': discount_amount,
        'discount_code': discount_code,
        'discount_percent': discount_percent,
    }

    return render(request, 'cart/checkout.html', context)


@login_required
def checkout_success(request, order_number):
    """
    Handle successful checkouts, clear session cart and discounts, and
    display confirmation.

    Args:
        request: HttpRequest object.
        order_number: The order number to confirm.

    Returns:
        Rendered checkout success page.
    """
    order = get_object_or_404(
        Order,
        order_number=order_number,
        user_profile__user=request.user
    )

    messages.success(
        request,
        f'Order successfully processed! Your order number is {order_number}. '
        f'A confirmation email will be sent to {order.email}.'
    )

    # Clear cart and discount data from session
    for key in ['cart', 'discount_code', 'discount_percent']:
        request.session.pop(key, None)

    return render(request, 'cart/checkout_success.html', {'order': order})


@login_required
def get_latest_order_number(request):
    """
    Return the latest order number for the logged-in user as JSON.

    Returns:
        JsonResponse with 'order_number' or None if no orders found.
    """
    order = (
        Order.objects
        .filter(user_profile__user=request.user)
        .order_by('-date')
        .first()
    )
    return JsonResponse({
        'order_number': order.order_number if order else None
    })


@login_required
@require_GET
def get_order_number_by_pid(request, pid):
    """
    Return the order number associated with a given Stripe payment intent ID.

    Args:
        pid: Stripe payment intent ID.

    Returns:
        JsonResponse with 'order_number' or None.
    """
    try:
        order = Order.objects.get(
            stripe_pid=pid,
            user_profile__user=request.user
        )
        return JsonResponse({'order_number': order.order_number})
    except Order.DoesNotExist:
        return JsonResponse({'order_number': None})


@superuser_required
def discount_codes_management(request):
    """
    View and add discount codes (admin-style management).

    GET: Show all discount codes and a form to add new.
    POST: Validate and save new discount code.

    Returns:
        Rendered discount codes management page.
    """
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


@superuser_required
def edit_discount_code(request, code_id):
    """
    Edit an existing discount code.

    GET: Show form pre-filled.
    POST: Validate and save changes.

    Returns:
        Rendered edit discount code page or redirects on success.
    """
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


@superuser_required
def delete_discount_code(request, code_id):
    """
    Confirm and delete a discount code.

    GET: Show confirmation page.
    POST: Delete and redirect.

    Returns:
        Rendered delete confirmation or redirects on deletion.
    """
    code = get_object_or_404(DiscountCode, id=code_id)
    if request.method == 'POST':
        code.delete()
        messages.success(request, "Discount code deleted successfully")
        return redirect('discount_codes_management')

    return render(request, 'cart/delete_discount_code.html', {'code': code})
