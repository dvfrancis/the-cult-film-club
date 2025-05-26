from django.contrib import admin
from .models import Releases, Images, Rating


@admin.register(Releases)
class ReleaseAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'release_date', 'director', 'genre'
    )
    list_filter = (
        'genre', 'resolution'
    )
    search_fields = (
        'title', 'release_date', 'director', 'description', 'genre',
        'subgenre', 'resolution', 'special_features', 'edition',
        'censor_status', 'packaging'
    )
    ordering = ['title', 'release_date', 'director', 'genre']


@admin.register(Images)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'caption']
    list_filter = ['date_added']
    search_fields = ['title__title', 'caption']
    ordering = ['caption']


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'rating', 'date_added')
    list_filter = ('rating', 'date_added')
    search_fields = ('user__username', 'title__title', 'rating', 'review')
    ordering = ['user__username', 'title__title', 'rating']
