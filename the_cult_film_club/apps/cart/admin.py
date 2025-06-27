from django.contrib import admin
from .models import Order, OrderLineItem, DiscountCode


class OrderLineItemAdminInline(admin.TabularInline):
    """
    Inline admin interface for order line items,
    displayed within the Order admin page.
    """
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)
    extra = 0  # Prevent extra empty forms


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin interface for Orders,
    including inline display of related order line items.
    """
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = (
        'order_number', 'date',
        'delivery_cost', 'subtotal',
        'total', 'original_bag',
        'stripe_pid',
    )

    fields = (
        'order_number', 'date',
        ('full_name', 'email', 'phone_number'),
        ('country', 'postcode', 'town_or_city'),
        ('street_address1', 'street_address2', 'county'),
        'delivery_cost', 'subtotal', 'total',
        'original_bag', 'stripe_pid',
    )

    list_display = (
        'order_number', 'date', 'full_name',
        'subtotal', 'delivery_cost', 'total',
    )

    list_display_links = ('order_number', 'full_name')
    ordering = ('-date',)
    list_filter = ('date', 'country')
    search_fields = ('order_number', 'email', 'full_name')


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    """
    Admin interface for managing discount codes.
    """
    list_display = ('code', 'percent', 'valid_from', 'valid_to', 'is_active')
    search_fields = ('code',)
    list_filter = ('is_active', 'valid_from', 'valid_to')
