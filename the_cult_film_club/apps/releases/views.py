from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.db.models import Q
from .models import Releases


def releases(request):
    """
    Display all releases, including sort and search queries.
    """
    releases = Releases.objects.all().order_by('title')
    query = None
    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request,
                    "You didn't enter a search term!"
                )
                context = {
                    "releases": [],
                    "search_term": query,
                }
                return render(request, "releases/releases.html", context)
            queries = (
                Q(image__caption__icontains=query) |
                Q(title__icontains=query) |
                Q(release_date__icontains=query) |
                Q(director__icontains=query) |
                Q(description__icontains=query) |
                Q(genre__icontains=query) |
                Q(subgenre__icontains=query) |
                Q(resolution__icontains=query) |
                Q(special_features__icontains=query) |
                Q(edition__icontains=query) |
                Q(censor_status__icontains=query) |
                Q(packaging__icontains=query) |
                Q(copies_available__icontains=query) |
                Q(price__icontains=query)
            )
            releases = releases.filter(queries)
    context = {
            "releases": releases,
            "search_term": query,
        }
    return render(request, "releases/releases.html", context)


def release_details(request, release_id):
    """
    Display details of a release.
    """
    release = get_object_or_404(Releases, pk=release_id)
    context = {"release": release}
    return render(request, "releases/release_details.html", context)
