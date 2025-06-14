from django.contrib import admin
from .models import Order, OrderLineItem, DiscountCode


class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = ('order_number', 'date',
                       'delivery_cost', 'subtotal',
                       'total', 'original_bag',
                       'stripe_pid',)

    fields = ('order_number', 'date', 'full_name',
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'delivery_cost',
              'subtotal', 'total', 'original_bag',
              'stripe_pid',)

    list_display = ('order_number', 'date', 'full_name',
                    'subtotal', 'delivery_cost',
                    'total',)

    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'percent', 'valid_from', 'valid_to', 'is_active')
    search_fields = ('code',)
    list_filter = ('is_active', 'valid_from', 'valid_to')
