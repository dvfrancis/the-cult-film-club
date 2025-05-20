from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('the_cult_film_club.apps.home.urls')),
    path("admin/", admin.site.urls),
    path('accounts/', include('allauth.urls')),
]
