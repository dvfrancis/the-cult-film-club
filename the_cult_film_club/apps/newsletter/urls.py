from django.urls import path
from . import views

urlpatterns = [
    # Newsletter Signup Page
    path(
        '',
        views.newsletter_signup,
        name='newsletter_signup'
    ),

    # Unsubscribe via secure token
    path(
        'newsletter/unsubscribe/<uuid:token>/',
        views.unsubscribe,
        name='newsletter_unsubscribe'
    ),

    # Request unsubscribe link via email
    path(
        'newsletter/unsubscribe-request/',
        views.newsletter_unsubscribe_request,
        name='newsletter_unsubscribe_request'
    ),
    path(
        'newsletter/edit/<uuid:token>/',
        views.edit_newsletter_preferences,
        name='edit_newsletter_preferences'
    ),
]
