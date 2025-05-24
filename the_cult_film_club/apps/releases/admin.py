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
        'title', 'release_date', 'director', 'description', 'genre', 'subgenre',
        'resolution', 'special_features', 'edition',
        'censor_status', 'packaging'
    )
    ordering = ['title', 'release_date', 'director', 'genre']

    def get_images(self, obj):
        return ", ".join([str(img) for img in obj.image.all()])
    get_images.short_description = 'Images'


@admin.register(Images)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_filter = ['title']
    search_fields = ['title']
    ordering = ['title']


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'rating', 'review', 'date_added')
    list_filter = ('user', 'title', 'rating', 'review', 'date_added')
    search_fields = ('user__username', 'title__title', 'rating', 'review')
    ordering = ['user__username', 'title__title', 'rating']
