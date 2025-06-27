from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    # Shopping cart main page
    path("", views.shopping_cart, name="cart"),

    # Cart item management
    path("add/<int:item_id>/", views.add_to_cart, name="add_to_cart"),
    path("adjust/<int:item_id>/", views.amend_cart, name="amend_cart"),
    path(
        "remove/<int:item_id>/",
        views.remove_from_cart,
        name="remove_from_cart"
    ),

    # Discount code application
    path("apply_discount/", views.apply_discount, name="apply_discount"),

    # Checkout flow
    path("order/", views.checkout, name="checkout"),
    path(
        "checkout_success/<str:order_number>/",
        views.checkout_success,
        name="checkout_success"
    ),

    # Stripe webhook endpoint
    path("wh/", webhook, name="webhook"),

    # Cache checkout data for Stripe
    path(
        "cache_checkout_data/",
        views.cache_checkout_data,
        name="cache_checkout_data"
    ),

    # Order detail view
    path("order/<str:order_number>/", views.order_detail, name="order_detail"),

    # API endpoints for AJAX
    path(
        "get-latest-order-number/",
        views.get_latest_order_number,
        name="get_latest_order_number"
    ),
    path(
        "get-order-number-by-pid/<str:pid>/",
        views.get_order_number_by_pid,
        name="get_order_number_by_pid"
    ),

    # Discount codes management (admin style)
    path(
        "discount-codes/",
        views.discount_codes_management,
        name="discount_codes_management"
    ),
    path(
        "discount-codes/edit/<int:code_id>/",
        views.edit_discount_code,
        name="edit_discount_code"
    ),
    path(
        "discount-codes/delete/<int:code_id>/",
        views.delete_discount_code,
        name="delete_discount_code"
    ),
]
