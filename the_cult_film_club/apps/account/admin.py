from django.contrib import admin
from .models import Profile, Address, Wishlist


@admin.register(Profile, Address, Wishlist)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user']
    list_filter = ['user']
    search_fields = ['user__username']
    ordering = ['user__username']


class AddressAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'first_line', 'second_line',
        'city', 'county', 'postcode', 'country')
    list_filter = (
        'user', 'first_line', 'second_line',
        'city', 'county', 'postcode', 'country')
    search_fields = (
        'user__username', 'first_line', 'second_line',
        'city', 'county', 'postcode', 'country'
    )
    ordering = ['user__username', 'city']


class WishlistAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'title', 'notes', 'priority', 'quantity', 'is_purchased')
    list_filter = (
        'user', 'title', 'notes', 'priority', 'quantity', 'is_purchased')
    search_fields = ('user__username', 'title', 'notes', 'priority')
    ordering = ['user__username', 'title', 'notes', 'priority']
