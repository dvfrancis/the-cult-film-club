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
    path('manage/', views.product_management, name='product_management'),
    path('edit/<int:release_id>/', views.edit_release, name='edit_release'),
    path(
        'delete/<int:release_id>/',
        views.delete_release,
        name='delete_release'
    ),
    path(
        'images/<int:release_id>/',
        views.manage_images,
        name='manage_images'
    ),
    path(
        'images/delete/<int:image_id>/',
        views.delete_image,
        name='delete_image'
    ),
    path(
        'wishlist/add/<int:release_id>/',
        views.add_to_wishlist,
        name='add_to_wishlist'
    ),
    path(
        'release/<int:release_id>/delete_rating/',
        views.delete_rating,
        name='delete_rating'
    ),
]
