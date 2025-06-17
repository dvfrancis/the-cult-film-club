from django.urls import path
from .views import newsletter_signup
from . import views

urlpatterns = [
    path('', newsletter_signup, name='newsletter_signup'),
    path(
        'newsletter/unsubscribe/<uuid:token>/',
        views.unsubscribe,
        name='newsletter_unsubscribe'
    ),
    path(
        'newsletter/unsubscribe-request/',
        views.newsletter_unsubscribe_request,
        name='newsletter_unsubscribe_request'
    ),
]
