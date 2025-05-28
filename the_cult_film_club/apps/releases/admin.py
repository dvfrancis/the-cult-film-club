from django.contrib import admin
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Releases, Images, Rating


class ReleasesAdminForm(forms.ModelForm):
    class Meta:
        model = Releases
        fields = "__all__"
        widgets = {
            "description": CKEditor5Widget(config_name="extends"),
            "special_features": CKEditor5Widget(config_name="extends"),
        }


class RatingAdminForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = "__all__"
        widgets = {
            "review": CKEditor5Widget(config_name="extends"),
        }


@admin.register(Releases)
class ReleaseAdmin(admin.ModelAdmin):
    form = ReleasesAdminForm
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
    form = RatingAdminForm
    list_display = ('user', 'title', 'rating', 'date_added')
    list_filter = ('rating', 'date_added')
    search_fields = ('user__username', 'title__title', 'rating', 'review')
    ordering = ['user__username', 'title__title', 'rating']