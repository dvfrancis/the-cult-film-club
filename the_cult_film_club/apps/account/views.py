from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Profile, Address, Wishlist, WishlistItem
from the_cult_film_club.apps.cart.models import Order
from .forms import ProfilePhotoForm, AddressForm, WishlistItemForm
from the_cult_film_club.apps.releases.models import Releases
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import logout


@login_required
def user_profile(request: HttpRequest) -> HttpResponse:
    """
    Display and manage the user's profile, addresses, wishlist, and orders
    """
    user_profile = get_object_or_404(Profile, user=request.user)
    orders = (
        Order.objects
        .filter(user_profile__user=request.user)
        .order_by('-date')
    )
    addresses = Address.objects.filter(user=request.user)
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    wishlist_items = (
        WishlistItem.objects
        .filter(wishlist=wishlist)
        .select_related('title')
    )

    if 'delete_account' in request.POST:
        user = request.user
        logout(request)  # Logs out user immediately
        # Cascades delete to Profile, Orders, Addresses, Wishlist, etc.
        user.delete()
        messages.success(
            request,
            (
                "Your account and all associated data have been "
                "permanently deleted."
            )
        )
        return redirect('home')

    # Default form for GET or fallback
    form = WishlistItemForm()
    form.fields['title'].queryset = Releases.objects.exclude(
        id__in=wishlist.title.values_list('id', flat=True)
    )

    # Handle POST actions
    if request.method == 'POST':
        # Profile photo update
        if 'update_photo' in request.POST:
            photo_form = ProfilePhotoForm(
                request.POST, request.FILES, instance=user_profile
            )
            if photo_form.is_valid():
                photo_form.save()
                messages.success(request, "Profile photo updated successfully")
            return redirect('user_profile')

        # Add address
        if 'add_address' in request.POST:
            address_form = AddressForm(request.POST)
            if address_form.is_valid():
                address = address_form.save(commit=False)
                address.user = request.user
                if not addresses.filter(default_address=True).exists():
                    address.default_address = True
                address.save()
                messages.success(request, "Address added successfully")
            return redirect('user_profile')

        # Update address
        if 'update_address' in request.POST:
            selected_address_id = request.POST.get('address')
            selected_address = addresses.filter(id=selected_address_id).first()
            address_form = AddressForm(request.POST, instance=selected_address)
            if address_form.is_valid():
                if not address_form.cleaned_data.get('default_address'):
                    other_defaults = (
                        addresses.filter(default_address=True)
                        .exclude(id=selected_address.id)
                    )
                    if not other_defaults.exists():
                        messages.error(
                            request,
                            (
                                "At least one address must be set as default"
                            )
                        )
                        return redirect(
                            f"{request.path}?address={selected_address.id}"
                        )
                address_form.save()
                messages.success(request, "Address updated successfully")
            return redirect(f"{request.path}?address={selected_address.id}")

        # Delete address
        if 'delete_address' in request.POST:
            selected_address_id = request.POST.get('address')
            selected_address = addresses.filter(id=selected_address_id).first()
            if addresses.count() <= 1:
                messages.error(
                    request,
                    (
                        (
                            (
                                (
                                    (
                                        "You must have at least one address - "
                                        "add another before deleting this one"
                                    )
                                )
                            )
                        )
                    )
                )
                return redirect('user_profile')
            was_default = selected_address.default_address
            selected_address.delete()
            remaining = Address.objects.filter(user=request.user)
            if was_default and remaining.exists():
                first_address = remaining.first()
                first_address.default_address = True
                first_address.save()
            messages.success(request, "Address deleted successfully")
            return redirect('user_profile')

        # Remove wishlist item
        if 'remove_item' in request.POST:
            item_id = request.POST.get('remove_item')
            wishlist_item = (
                WishlistItem.objects
                .filter(id=item_id, wishlist=wishlist)
                .first()
            )
            if wishlist_item:
                title = wishlist_item.title
                wishlist_item.delete()
                messages.success(
                    request,
                    f"{title} has been removed from your wishlist"
                )
            else:
                messages.error(request, "Wishlist item not found")
            return redirect('user_profile')

        # Add wishlist item
        if 'add_item' in request.POST:
            form = WishlistItemForm(request.POST)
            form.fields['title'].queryset = Releases.objects.exclude(
                id__in=wishlist.title.values_list('id', flat=True)
            )
            if form.is_valid():
                wishlist_item = form.save(commit=False)
                wishlist_item.wishlist = wishlist
                wishlist_item.save()
                messages.success(
                    request,
                    f"{wishlist_item.title} has been added to your wishlist"
                )
            return redirect('user_profile')

    # Address selection logic for GET or after POST
    selected_address_id = (
        request.GET.get('address') or request.POST.get('address')
    )
    if selected_address_id == "new":
        selected_address = None
    elif selected_address_id:
        selected_address = addresses.filter(id=selected_address_id).first()
    else:
        selected_address = addresses.filter(default_address=True).first()

    address_form = (
        AddressForm(instance=selected_address)
        if selected_address else AddressForm()
    )
    photo_form = ProfilePhotoForm(instance=user_profile)

    context = {
        'user_profile': user_profile,
        'orders': orders,
        'photo_form': photo_form,
        'addresses': addresses,
        'selected_address': selected_address,
        'address_form': address_form,
        'wishlist_items': wishlist_items,
        'form': form,
    }
    return render(request, 'account/account.html', context)
