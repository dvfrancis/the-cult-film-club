from django.apps import AppConfig


class AccountConfig(AppConfig):
    """
    Configuration class for the 'account' app within 'the_cult_film_club'

    This sets a custom label for internal Django app registry and a
    user-friendly verbose name for the admin interface
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "the_cult_film_club.apps.account"

    # Custom label used to avoid app name conflicts in complex projects
    label = "the_cult_film_club_account"

    # Display name for the app in the Django admin
    verbose_name = "User Profiles"
