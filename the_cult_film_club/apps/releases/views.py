from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Avg, F, Value
from .models import Releases
from django.core.paginator import Paginator
from django.db.models.functions import Length, Substr, Reverse, StrIndex


def releases(request):
    releases_list = Releases.objects.all()
    query = None
    sort = None
    direction = None

    # Search logic
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
        releases_list = releases_list.filter(queries)

    # Sorting logic (always runs)
    if 'sort' in request.GET:
        sort = request.GET['sort']
        sortkey = sort
        if sort == 'price':
            sortkey = 'price'
        elif sort == 'director_last':
            releases_list = releases_list.annotate(
                rev_dir=Reverse('director'),
                last_space_pos=StrIndex(Reverse('director'), Value(' ')),
            ).annotate(
                last_name=Substr(
                    'director',
                    Length('director') - (F('last_space_pos') - 1),
                    Length('director')
                )
            )
            sortkey = 'last_name'
        elif sort == 'rating':
            releases_list = releases_list.annotate(
                avg_rating=Avg('ratings__rating')
            )
            sortkey = 'avg_rating'
        # Direction
        if 'direction' in request.GET:
            direction = request.GET['direction']
            if direction == 'desc':
                releases_list = releases_list.order_by(
                    F(sortkey).desc(nulls_last=True)
                )
            else:
                releases_list = releases_list.order_by(
                    F(sortkey).asc(nulls_first=True)
                )
        else:
            releases_list = releases_list.order_by(sortkey)
    else:
        # Default to alphabetical by title, when no sort is specified
        releases_list = releases_list.order_by('title')

    paginator = Paginator(releases_list, 8)
    page_number = request.GET.get('page')
    releases = paginator.get_page(page_number)

    querydict = request.GET.copy()
    if 'page' in querydict:
        querydict.pop('page')
    querystring = querydict.urlencode()

    context = {
        "releases": releases,
        "search_term": query,
        "current_sort": sort,
        "current_direction": direction,
        "querystring": querystring,
    }
    return render(request, "releases/releases.html", context)


def release_details(request, release_id):
    """
    Display details of a release.
    """
    release = get_object_or_404(Releases, pk=release_id)
    context = {"release": release}
    return render(request, "releases/release_details.html", context)
