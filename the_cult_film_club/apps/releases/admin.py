from django.contrib import admin
from django.utils.html import format_html
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Releases, Images, Rating


class ReleasesAdminForm(forms.ModelForm):
    """Custom form for Releases admin with CKEditor widgets for text fields."""
    class Meta:
        model = Releases
        fields = "__all__"
        widgets = {
            "description": CKEditor5Widget(config_name="default"),
            "special_features": CKEditor5Widget(config_name="default"),
        }


class RatingAdminForm(forms.ModelForm):
    """Custom form for Rating admin with CKEditor widget for review."""
    class Meta:
        model = Rating
        fields = "__all__"
        widgets = {
            "review": CKEditor5Widget(config_name="default"),
        }


class ImageInline(admin.TabularInline):
    """Inline admin to manage Images related to a Release."""
    model = Images
    extra = 0


class RatingInline(admin.TabularInline):
    """Inline admin to manage Ratings related to a Release."""
    model = Rating
    form = RatingAdminForm
    extra = 0


@admin.register(Releases)
class ReleaseAdmin(admin.ModelAdmin):
    """
    Admin configuration for Releases model including inlines for Images and
    Ratings. Displays key fields and renders description and special features
    as HTML.
    """
    form = ReleasesAdminForm
    inlines = [ImageInline, RatingInline]

    list_display = (
        'title',
        'release_date',
        'director',
        'genre',
        'description_html',
        'special_features_html',
    )
    list_filter = ('genre', 'resolution')
    search_fields = (
        'title', 'release_date', 'director', 'description', 'genre',
        'subgenre', 'resolution', 'special_features', 'edition',
        'censor_status', 'packaging'
    )
    ordering = ['title', 'release_date', 'director', 'genre']
    readonly_fields = ('description_html', 'special_features_html')

    def description_html(self, obj):
        """Render description field as safe HTML in admin detail view."""
        return format_html(obj.description)
    description_html.short_description = 'Description'

    def special_features_html(self, obj):
        """Render special features field as safe HTML in admin detail view."""
        return format_html(obj.special_features)
    special_features_html.short_description = 'Special Features'
