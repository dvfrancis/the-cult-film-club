from django.urls import path
from . import views

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
    path("checkout/", views.checkout, name="checkout"),
]
