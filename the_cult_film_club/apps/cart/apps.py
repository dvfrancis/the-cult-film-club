from django.apps import AppConfig


class CartConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "the_cult_film_club.apps.cart"
    verbose_name = "Shop"

    def ready(self):
        from the_cult_film_club.apps.cart import signals  # noqa: F401
