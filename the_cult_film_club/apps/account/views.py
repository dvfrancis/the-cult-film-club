from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Profile, Address, Wishlist, WishlistItem
from the_cult_film_club.apps.cart.models import Order
from .forms import ProfilePhotoForm, AddressForm, WishlistItemForm
from the_cult_film_club.apps.releases.models import Releases
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import logout
import cloudinary.uploader


@login_required
def user_profile(request: HttpRequest) -> HttpResponse:
    """
    Display and manage the user's profile, addresses, wishlist, and orders,
    including editing wishlist items.
    """
    user_profile = get_object_or_404(Profile, user=request.user)
    orders = (
        Order.objects
        .filter(user_profile__user=request.user)
        .order_by('-date')
    )
    addresses = Address.objects.filter(user=request.user)
    wishlists = Wishlist.objects.filter(user=request.user)
    selected_wishlist_id = (
        request.GET.get("wishlist") or request.POST.get("wishlist")
    )
    selected_wishlist = (
        wishlists.filter(id=selected_wishlist_id).first()
        if selected_wishlist_id else wishlists.first()
    )
    wishlist = selected_wishlist

    # Handle wishlist items (empty if no wishlist selected)
    wishlist_items = (
        WishlistItem.objects.filter(wishlist=wishlist)
        .select_related('title')
        if wishlist else []
    )

    # === Handle creating wishlist ===
    if 'create_wishlist' in request.POST:
        name = request.POST.get('wishlist_name', '').strip()
        if not name:
            messages.error(request, 'Wishlist name cannot be blank.')
        else:
            exists = wishlists.filter(name__iexact=name).exists()
            if exists:
                messages.error(
                    request,
                    f'You already have a wishlist called "{name}".'
                )
            else:
                Wishlist.objects.create(user=request.user, name=name)
                messages.success(request, f'Wishlist "{name}" created.')
        return redirect('user_profile')

    # === Delete wishlist ===
    if 'delete_wishlist' in request.POST:
        wishlist_id = request.POST.get("wishlist")
        wishlist_to_delete = wishlists.filter(id=wishlist_id).first()
        if wishlist_to_delete:
            wishlist_to_delete.delete()
            messages.success(request, "Wishlist deleted.")
        else:
            messages.error(request, "Wishlist not found.")
        return redirect('user_profile')

    # === Delete profile photo ===
    if 'delete_photo' in request.POST:
        if (
            user_profile.photograph and
            user_profile.photograph.public_id != 'placeholder'
        ):
            cloudinary.uploader.destroy(user_profile.photograph.public_id)
            user_profile.photograph = 'placeholder'
            user_profile.save()
            messages.success(request, "Profile photo deleted.")
        else:
            messages.info(request, "No photo to delete")
        return redirect('user_profile')

    # === Delete account ===
    if 'delete_account' in request.POST:
        user = request.user
        logout(request)  # Logs out user immediately
        user.delete()
        messages.success(
            request,
            (
                "Your account and all associated data have been "
                "permanently deleted."
            )
        )
        return redirect('home')

    # === Default wishlist item form (for add) ===
    add_form = WishlistItemForm()
    if wishlist:
        add_form.fields['title'].queryset = Releases.objects.exclude(
            id__in=wishlist.title.values_list('id', flat=True)
        )
    else:
        add_form.fields['title'].queryset = Releases.objects.all()

    # === Handle editing wishlist item ===
    edit_item_id = (
        request.GET.get('edit_item') or request.POST.get('edit_item')
    )
    if edit_item_id:
        wishlist_item = get_object_or_404(
            WishlistItem,
            id=edit_item_id,
            wishlist__user=request.user  # ensure ownership
        )
        if request.method == 'POST' and 'edit_item' in request.POST:
            edit_form = WishlistItemForm(request.POST, instance=wishlist_item)
            # Exclude all other wishlist items' titles except this one's title
            edit_form.fields['title'].queryset = Releases.objects.exclude(
                id__in=WishlistItem.objects
                .filter(wishlist=wishlist_item.wishlist)
                .exclude(id=wishlist_item.id)
                .values_list('title_id', flat=True)
            )
            if edit_form.is_valid():
                edit_form.save()
                messages.success(
                    request,
                    f'Wishlist item "{wishlist_item.title}" updated.'
                )
                return redirect(f"{request.path}?wishlist={wishlist.id}")
        else:
            edit_form = WishlistItemForm(instance=wishlist_item)
            edit_form.fields['title'].queryset = Releases.objects.exclude(
                id__in=WishlistItem.objects
                .filter(wishlist=wishlist_item.wishlist)
                .exclude(id=wishlist_item.id)
                .values_list('title_id', flat=True)
            )

        context = {
            'user_profile': user_profile,
            'orders': orders,
            'addresses': addresses,
            'wishlists': wishlists,
            'selected_wishlist': selected_wishlist,
            'wishlist_items': wishlist_items,
            'edit_mode': True,
            'edit_form': edit_form,
            'edit_item': wishlist_item,
            'photo_form': ProfilePhotoForm(instance=user_profile),
            'address_form': AddressForm(instance=None),
            'form': add_form,
        }
        return render(request, 'account/account.html', context)

    # === Handle other POST actions ===
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
                            "At least one address must be set as default"
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
                    f'"{title}" has been removed from your wishlist'
                )
            else:
                messages.error(request, "Wishlist item not found")
            return redirect('user_profile')

        # Add wishlist item
        if 'add_item' in request.POST:
            wishlist = wishlists.filter(
                id=request.POST.get("wishlist")
            ).first()
            add_form = WishlistItemForm(request.POST)
            add_form.fields['title'].queryset = Releases.objects.exclude(
                id__in=wishlist.title.values_list('id', flat=True)
            )
            if add_form.is_valid():
                wishlist_item = add_form.save(commit=False)
                wishlist_item.wishlist = wishlist
                wishlist_item.save()
                messages.success(
                    request,
                    f'"{wishlist_item.title}" has been added to your wishlist'
                )
            return redirect(f"{request.path}?wishlist={wishlist.id}")

    # === Address form preparation ===
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
        'addresses': addresses,
        'selected_address': selected_address,
        'address_form': address_form,
        'photo_form': photo_form,
        'wishlist_items': wishlist_items,
        'form': add_form,
        'wishlists': wishlists,
        'selected_wishlist': selected_wishlist,
    }
    return render(request, 'account/account.html', context)
