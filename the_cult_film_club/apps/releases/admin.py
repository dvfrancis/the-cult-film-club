from django.contrib import admin
from django.utils.html import format_html
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


class ImageInline(admin.TabularInline):
    model = Images
    extra = 1


class RatingInline(admin.TabularInline):
    model = Rating
    form = RatingAdminForm
    extra = 1


@admin.register(Releases)
class ReleaseAdmin(admin.ModelAdmin):
    form = ReleasesAdminForm
    inlines = [ImageInline, RatingInline]
    list_display = (
        'title', 'release_date', 'director', 'genre', 'description_html'
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

    def description_html(self, obj):
        return format_html(obj.description)
    description_html.short_description = 'Description'

    def special_features_html(self, obj):
        return format_html(obj.special_features)
    special_features_html.short_description = 'Special Features'
