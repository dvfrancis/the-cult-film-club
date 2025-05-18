from django.contrib import admin
from .models import Releases, Images, Rating


@admin.register(Releases)
class ReleaseAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'release_date', 'genre', 'subgenre',
        'resolution', 'resolution', 'edition', 'packaging', 'image'
    )
    list_filter = (
        'title', 'release_date', 'description', 'genre', 'subgenre',
        'resolution', 'edition', 'packaging'
    )
    search_fields = (
        'title', 'release_date', 'description', 'genre', 'subgenre',
        'resolution', 'special_features', 'edition',
        'censor_status', 'packaging'
    )
    ordering = ['title', 'release_date', 'genre', 'subgenre']


@admin.register(Images)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'title')
    list_filter = ('image', 'title')
    search_fields = ('image', 'title')
    ordering = ['image', 'title']


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):        
    list_display = ('user', 'title', 'rating', 'review', 'date_added')
    list_filter = ('user', 'title', 'rating', 'review', 'date_added')
    search_fields = ('user__username', 'title__title', 'rating', 'review')
    ordering = ['user__username', 'title__title', 'rating']
