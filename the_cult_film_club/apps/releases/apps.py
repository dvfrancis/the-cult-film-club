from django.apps import AppConfig


class ReleasesConfig(AppConfig):
    """
    Configuration for the Releases app, handling film releases and related
    models.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "the_cult_film_club.apps.releases"
    verbose_name = "Films"
