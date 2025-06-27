from django.shortcuts import render
from the_cult_film_club.apps.releases.models import Releases


def index(request):
    """
    Display the home page for The Cult Film Club.

    This view fetches and displays 3 random cult film releases to
    highlight on the homepage.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: The rendered home page with context data.
    """
    featured_releases = Releases.objects.order_by('?')[:3]
    return render(request, 'home/index.html', {
        'releases': featured_releases
    })
