from django.shortcuts import render
from .models import Releases


def all_releases(request):
    """
    Display all releases.
    """
    releases = Releases.objects.all().order_by('title')
    context = {"releases": releases}
    return render(request, "releases/releases.html", context)
