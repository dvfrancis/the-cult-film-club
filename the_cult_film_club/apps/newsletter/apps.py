from django.apps import AppConfig


class NewsletterConfig(AppConfig):
    """
    Configuration for the Newsletter app.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "the_cult_film_club.apps.newsletter"
    verbose_name = "Newsletter"
