from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from django.http import HttpResponseBadRequest
from django.core.exceptions import PermissionDenied


def custom_bad_request(request, exception):
    return render(request, "error_pages/bad_request.html", status=400)


def custom_permission_denied(request, exception):
    return render(request, "error_pages/permission_denied.html", status=403)


def custom_page_not_found(request, exception):
    return render(request, "error_pages/page_not_found.html", status=404)


def custom_server_error(request):
    return render(request, "error_pages/server_error.html", status=500)


def raise_server_error(request):
    raise Exception("Test 500 error")


def raise_permission_denied(request):
    raise PermissionDenied


def raise_bad_request(request):
    return HttpResponseBadRequest()


handler400 = custom_bad_request
handler403 = custom_permission_denied
handler404 = custom_page_not_found
handler500 = custom_server_error


urlpatterns = [
    path("", include("the_cult_film_club.apps.home.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("releases/", include("the_cult_film_club.apps.releases.urls")),
    path("checkout/", include("the_cult_film_club.apps.cart.urls")),
    path("account/", include("the_cult_film_club.apps.account.urls")),
    path('test-400/', raise_bad_request, name='raise_bad_request'),
    path('test-403/', raise_permission_denied, name='raise_permission_denied'),
    path('test-500/', raise_server_error, name='raise_server_error'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
