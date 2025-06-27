"""
App configuration for the 'home' app of The Cult Film Club project.
"""

from django.apps import AppConfig


class HomeConfig(AppConfig):
    # Specifies the type of primary key to use for models in this app
    default_auto_field = "django.db.models.BigAutoField"

    # Full Python path to the application
    name = "the_cult_film_club.apps.home"

    # Human-readable name for admin site and introspection tools
    verbose_name = "Home"
