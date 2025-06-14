from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path("", views.shopping_cart, name="cart"),
    path("add/<item_id>/", views.add_to_cart, name="add_to_cart"),
    path("adjust/<item_id>/", views.amend_cart, name="amend_cart"),
    path("remove/<item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path(
        "set_delivery_option/",
        views.set_delivery_option,
        name="set_delivery_option"
    ),
    path("apply_discount/", views.apply_discount, name="apply_discount"),
    path("order/", views.checkout, name="checkout"),
    path(
        "checkout_success/<order_number>/",
        views.checkout_success,
        name="checkout_success"
    ),
    path("wh/", webhook, name="webhook"),
    path(
        "cache_checkout_data/",
        views.cache_checkout_data,
        name="cache_checkout_data"
    ),
    path('order/<order_number>/', views.order_detail, name='order_detail'),
    path(
        "get-latest-order-number/",
        views.get_latest_order_number,
        name="get_latest_order_number"
    ),
    path(
        'get-order-number-by-pid/<str:pid>/',
        views.get_order_number_by_pid,
        name='get_order_number_by_pid'
    ),
    path(
        'discount-codes/',
        views.discount_codes_management,
        name='discount_codes_management'
    ),
    path(
        'discount-codes/edit/<int:code_id>/',
        views.edit_discount_code,
        name='edit_discount_code'
    ),
    path(
        'discount-codes/delete/<int:code_id>/',
        views.delete_discount_code,
        name='delete_discount_code'
    ),
]
