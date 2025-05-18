from django.contrib import admin
from .models import Releases


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
