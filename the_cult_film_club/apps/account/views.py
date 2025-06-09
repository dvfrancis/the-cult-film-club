from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Profile, Address
from the_cult_film_club.apps.cart.models import Order
from .forms import ProfilePhotoForm, AddressForm


def user_profile(request):
    user_profile = get_object_or_404(Profile, user=request.user)
    orders = (
        Order.objects
        .filter(user_profile__user=request.user)
        .order_by('-date')
    )
    addresses = Address.objects.filter(user=request.user)

    if request.method == 'POST':
        if 'update_photo' in request.POST:
            photo_form = ProfilePhotoForm(
                request.POST, request.FILES, instance=user_profile
            )
            if photo_form.is_valid():
                photo_form.save()
                messages.success(request, "Profile photo updated successfully")
                return redirect('user_profile')

    # Determine selected address (for update/delete)
    selected_address_id = (
        request.GET.get('address') or request.POST.get('address')
    )

    if selected_address_id == "new":
        selected_address = None
    elif selected_address_id:
        selected_address = addresses.filter(id=selected_address_id).first()
    else:
        # On first page load, show default address if exists
        selected_address = addresses.filter(default_address=True).first()

    # Handle form actions
    if request.method == 'POST':
        if 'add_address' in request.POST:
            address_form = AddressForm(request.POST)
            if address_form.is_valid():
                address = address_form.save(commit=False)
                address.user = request.user
                # If this is the first address or no default exists,
                # set as default
                if not addresses.filter(default_address=True).exists():
                    address.default_address = True
                address.save()
                messages.success(request, "Address added successfully")
                return redirect('user_profile')
        elif 'update_address' in request.POST and selected_address:
            address_form = AddressForm(request.POST, instance=selected_address)
            if address_form.is_valid():
                address_form.save()
                messages.success(request, "Address updated successfully")
                return redirect(
                    f"{request.path}?address={selected_address.id}"
                )
        elif 'delete_address' in request.POST and selected_address:
            was_default = selected_address.default_address
            selected_address.delete()
            # If the deleted address was default, set another as default
            if was_default:
                remaining = Address.objects.filter(user=request.user)
                if remaining.exists():
                    first_address = remaining.first()
                    first_address.default_address = True
                    first_address.save()
            messages.success(request, "Address deleted successfully")
            return redirect('user_profile')
        else:
            address_form = (
                AddressForm(instance=selected_address)
                if selected_address else AddressForm()
            )
    else:
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
    }
    return render(request, 'account/account.html', context)
