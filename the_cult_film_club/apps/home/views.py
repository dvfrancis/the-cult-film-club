from django.shortcuts import render
from the_cult_film_club.apps.releases.models import Releases


def index(request):
    """
    Render the home page of the Cult Film Club with 3 random releases.
    """
    releases = Releases.objects.order_by('?')[:3]  # Get 3 random releases
    return render(request, 'home/index.html', {'releases': releases})
