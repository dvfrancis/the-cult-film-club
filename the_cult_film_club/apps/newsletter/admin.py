from django.contrib import admin
from the_cult_film_club.apps.newsletter.models import NewsletterSignup


@admin.register(NewsletterSignup)
class NewsletterSignupAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'display_genres',
        'date_joined',
        'unsubscribe_token',
    )
    list_filter = ('date_joined',)
    search_fields = ('email',)
    ordering = ['-date_joined']

    def display_genres(self, obj):
        """Display genres as a comma-separated list with better formatting."""
        return ", ".join(obj.genres.split(',')) if obj.genres else "-"
    display_genres.short_description = 'Genres'
