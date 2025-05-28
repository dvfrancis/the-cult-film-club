from django.contrib import admin
from .models import ContactUs
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget


class ContactUsAdminForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = "__all__"
        widgets = {
            "message": CKEditor5Widget(config_name="extends"),
        }


@admin.register(ContactUs)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'message')
    list_filter = ('first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name', 'email', 'message')
    ordering = ['first_name', 'last_name', 'email']
