from django.shortcuts import render, get_object_or_404
from .models import Releases


def releases(request):
    """
    Display all releases.
    """
    releases = Releases.objects.all().order_by('title')
    context = {"releases": releases}
    return render(request, "releases/releases.html", context)


def release_details(request, release_id):
    """
    Display details of a release.
    """
    release = get_object_or_404(Releases, pk=release_id)
    context = {"release": release}
    return render(request, "releases/release_details.html", context)
