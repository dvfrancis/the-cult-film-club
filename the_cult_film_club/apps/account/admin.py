from django.contrib import admin
from .models import Profile, Address, Wishlist


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user']
    list_filter = ['user']
    search_fields = ['user__username']
    ordering = ['user__username']


@admin.register(Address)
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


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'get_titles', 'notes', 'priority', 'quantity', 'is_purchased')
    list_filter = (
        'user', 'priority', 'quantity', 'is_purchased')
    search_fields = ('user__username', 'notes', 'priority')
    ordering = ['user__username', 'notes', 'priority']

    def get_titles(self, obj):
        return ", ".join([str(t) for t in obj.title.all()])
    get_titles.short_description = 'Titles'
