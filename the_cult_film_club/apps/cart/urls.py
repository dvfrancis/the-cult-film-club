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
]
