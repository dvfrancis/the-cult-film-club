import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "the_cult_film_club.settings")

application = get_asgi_application()
