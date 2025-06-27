from django.apps import AppConfig


class CartConfig(AppConfig):
    """
    Configuration for the Cart app,
    including registration of signals on app ready.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "the_cult_film_club.apps.cart"
    verbose_name = "Shop"

    def ready(self):
        """
        Import signals to ensure signal handlers are connected
        when the app is ready.
        """
        # Importing signals here to register signal handlers
        from the_cult_film_club.apps.cart import signals  # noqa: F401
