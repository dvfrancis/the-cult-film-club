from django.contrib import admin
from the_cult_film_club.apps.newsletter.models import NewsletterSignup


@admin.register(NewsletterSignup)
class NewsletterSignupAdmin(admin.ModelAdmin):
    list_display = ('email', 'genres', 'date_joined', 'unsubscribe_token')
    list_filter = ('genres', 'date_joined')
    search_fields = ('email', 'date_joined')
    ordering = ['date_joined']
