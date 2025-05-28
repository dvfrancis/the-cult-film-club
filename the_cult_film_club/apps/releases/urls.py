from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.releases, name='releases'),
    path(
        'release_details/<int:release_id>/',
        views.release_details,
        name='release_details'
    ),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
]
