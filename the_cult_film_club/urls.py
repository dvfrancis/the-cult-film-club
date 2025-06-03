from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include("the_cult_film_club.apps.home.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("releases/", include("the_cult_film_club.apps.releases.urls")),
    path("cart/", include("the_cult_film_club.apps.cart.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
