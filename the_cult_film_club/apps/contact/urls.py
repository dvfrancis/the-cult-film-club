from django.urls import path
from .views import contact_us

urlpatterns = [
    # Route for the Contact Us page, mapped to the contact_us view
    path('', contact_us, name='contact_us'),
]
