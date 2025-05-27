from django.urls import path
from . import views


urlpatterns = [
    path('', views.releases, name='releases'),
    path(
        'release_details/<int:release_id>/',
        views.release_details,
        name='release_details'
    ),
]
