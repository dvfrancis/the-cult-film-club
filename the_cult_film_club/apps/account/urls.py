from django.urls import path
from . import views
from the_cult_film_club.apps.cart import views as cart_views


urlpatterns = [
    path("user_profile/", views.user_profile, name="user_profile"),
    path('add/<int:item_id>/', cart_views.add_to_cart, name='add_to_cart')
]
