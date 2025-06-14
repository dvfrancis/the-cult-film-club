from django.contrib import admin
from .models import Profile, Address, Wishlist, WishlistItem
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from django.utils.html import format_html


class WishlistItemAdminForm(forms.ModelForm):
    class Meta:
        model = WishlistItem
        fields = "__all__"
        widgets = {
            "notes": CKEditor5Widget(config_name="extends"),
        }


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


class WishlistItemInline(admin.TabularInline):
    model = WishlistItem
    extra = 1  # Number of empty forms to display
    autocomplete_fields = ['title']
    fields = ('title', 'date_added', 'priority', 'is_purchased', 'notes')
    readonly_fields = ('date_added',)


@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    form = WishlistItemAdminForm
    list_display = (
        'wishlist', 'title', 'priority', 'is_purchased', 'notes_html'
    )
    search_fields = ('wishlist__user__username', 'title__title')
    ordering = ['wishlist__user__username', 'title__title']

    def notes_html(self, obj):
        return format_html(obj.notes)
    notes_html.short_description = 'Notes'


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user']
    inlines = [WishlistItemInline]
    search_fields = ['user__username']
    ordering = ['user__username']
