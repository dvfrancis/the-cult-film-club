from django.contrib import admin
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import ContactUs


class ContactUsAdminForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = "__all__"
        widgets = {
            "message": CKEditor5Widget(config_name="extends"),
        }


@admin.register(ContactUs)
class ContactAdmin(admin.ModelAdmin):
    """
    Admin interface for ContactUs messages.
    """
    form = ContactUsAdminForm

    list_display = (
        'first_name',
        'last_name',
        'email',
        'short_message',
        'created',
    )
    list_filter = ('first_name', 'last_name', 'email', 'created')
    search_fields = ('first_name', 'last_name', 'email', 'message')
    ordering = ['-created']

    readonly_fields = ('created',)

    list_display_links = ('first_name', 'last_name', 'email')

    def short_message(self, obj):
        if len(obj.message) > 75:
            return obj.message[:75] + '...'
        return obj.message
    short_message.short_description = 'Message Preview'
