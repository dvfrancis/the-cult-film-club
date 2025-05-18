from django.contrib import admin
from .models import ContactUs


@admin.register(ContactUs)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'message')
    list_filter = ('first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name', 'email', 'message')
    ordering = ['first_name', 'last_name', 'email']
