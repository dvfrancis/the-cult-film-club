"""
App configuration for the 'home' app of The Cult Film Club project.
"""

from django.apps import AppConfig


class HomeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "the_cult_film_club.apps.home"
    verbose_name = "Home"
