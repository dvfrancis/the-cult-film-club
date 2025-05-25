from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "the_cult_film_club.apps.account"
    label = "the_cult_film_club_account"
    verbose_name = "User Profiles"
