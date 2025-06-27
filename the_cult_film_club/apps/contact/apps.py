from django.apps import AppConfig


class ContactConfig(AppConfig):
    """
    Configuration for the Contact app.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "the_cult_film_club.apps.contact"
    verbose_name = "Contact Form"
