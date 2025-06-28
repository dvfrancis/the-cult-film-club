import math
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from django.db.models import Q, Avg, F, Value
from django.core.paginator import Paginator
from django.db.models.functions import (
    Length, Substr, Reverse, StrIndex, ExtractYear
)
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe

from the_cult_film_club.apps.releases.models import Releases, Rating, Images
from the_cult_film_club.apps.account.models import Wishlist, WishlistItem
from the_cult_film_club.apps.account.forms import WishlistItemForm
from .forms import ReleaseForm, ReleaseEditForm, ImageForm, RatingForm
from django.core.exceptions import PermissionDenied
from functools import wraps


def superuser_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.get_full_path())
        if not request.user.is_superuser:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def releases(request):
    """
    Display a paginated list of releases with filtering, searching, and
    sorting options.
    """
    releases_list = Releases.objects.all()
    query = None
    sort = None
    direction = None

    # Filtering parameters
    genre = request.GET.get('genre')
    subgenre = request.GET.get('subgenre')
    director = request.GET.get('director')
    decade = request.GET.get('decade')

    if genre:
        releases_list = releases_list.filter(genre=genre)
    if subgenre:
        releases_list = releases_list.filter(subgenre=subgenre)
    if director:
        releases_list = releases_list.filter(director=director)
    if decade:
        try:
            decade_int = int(decade)
            releases_list = releases_list.annotate(
                year=ExtractYear('release_date')
            ).filter(
                year__gte=decade_int,
                year__lt=decade_int + 10
            )
        except ValueError:
            messages.error(request, "Invalid decade filter.")
            return redirect(reverse("releases"))

    # Filter dropdown data from filtered queryset for consistency
    genres = (
        releases_list.values_list('genre', flat=True)
        .distinct()
        .order_by('genre')
    )
    subgenres = (
        releases_list.values_list('subgenre', flat=True)
        .distinct()
        .order_by('subgenre')
    )
    directors = (
        releases_list.values_list('director', flat=True)
        .distinct()
        .order_by('director')
    )

    # Get decades for filter dropdown (from all releases)
    years = (
        Releases.objects
        .annotate(year=ExtractYear('release_date'))
        .values_list('year', flat=True)
    )
    decades = sorted(set((y // 10) * 10 for y in years if y))

    # Search
    if 'q' in request.GET:
        query = request.GET['q'].strip()
        if not query:
            messages.error(
                request,
                "You didn't enter a search term. Please try again."
            )
            return redirect(reverse("home"))
        search_filter = (
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
        releases_list = releases_list.filter(search_filter)

    # Sorting
    if 'sort' in request.GET:
        sort = request.GET['sort']
        sortkey = sort
        if sort == 'director_last':
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
        elif sort not in ['price', 'copies_available']:
            # Fallback to title if unknown sort field
            sortkey = 'title'

        direction = request.GET.get('direction', 'asc')
        if direction == 'desc':
            releases_list = releases_list.order_by(
                F(sortkey).desc(nulls_last=True)
            )
        else:
            releases_list = releases_list.order_by(
                F(sortkey).asc(nulls_first=True)
            )
    else:
        # Default alphabetical
        releases_list = releases_list.order_by('title')

    paginator = Paginator(releases_list, 8)
    page_number = request.GET.get('page')
    releases_page = paginator.get_page(page_number)

    querydict = request.GET.copy()
    querydict.pop('page', None)
    querystring = querydict.urlencode()

    # Gather all filters combinations for JS if needed
    all_filters = []
    for r in (
        Releases.objects
        .values("genre", "subgenre", "director", "release_date")
        .distinct()
    ):
        year = r["release_date"].year if r["release_date"] else None
        decade_val = (year // 10) * 10 if year else None
        all_filters.append({
            "genre": r["genre"],
            "subgenre": r["subgenre"],
            "director": r["director"],
            "decade": decade_val,
        })

    context = {
        "releases": releases_page,
        "search_term": query,
        "current_sort": sort,
        "current_direction": direction,
        "querystring": querystring,
        "genres": genres,
        "subgenres": subgenres,
        "decades": decades,
        "directors": directors,
        "all_filters": all_filters,
    }
    return render(request, "releases/releases.html", context)


def release_details(request, release_id: int):
    """
    Display detailed information about a release, handle user ratings and
    wishlist addition.
    """
    release = get_object_or_404(Releases, pk=release_id)
    wishlist_form = WishlistItemForm()
    user_rating = None

    # Calculate star ratings
    average_rating = release.average_rating or 0
    full_stars = math.floor(average_rating)
    has_half_star = (average_rating - full_stars) >= 0.5
    empty_stars = 5 - full_stars - (1 if has_half_star else 0)

    # Navigation to next and previous releases
    next_release = (
        Releases.objects
        .filter(pk__gt=release.pk)
        .order_by('pk')
        .first()
    )
    prev_release = (
        Releases.objects
        .filter(pk__lt=release.pk)
        .order_by('-pk')
        .first()
    )

    if request.user.is_authenticated:
        user_rating = (
            Rating.objects
            .filter(user=request.user, title=release)
            .first()
        )

        if request.method == 'POST' and 'rating_submit' in request.POST:
            rating_form = RatingForm(request.POST, instance=user_rating)
            if rating_form.is_valid():
                rating = rating_form.save(commit=False)
                rating.user = request.user
                rating.title = release
                rating.save()
                messages.success(
                    request,
                    "Your rating has been submitted. Thank you!"
                )
                return redirect('release_details', release_id=release.id)
        else:
            rating_form = RatingForm(instance=user_rating)
    else:
        rating_form = None

    context = {
        "release": release,
        "rating_form": rating_form,
        "wishlist_form": wishlist_form,
        "user_rating": user_rating,
        "next_release": next_release,
        "prev_release": prev_release,
        "full_stars_range": range(full_stars),
        "empty_stars_range": range(empty_stars),
        "has_half_star": has_half_star,
    }
    return render(request, "releases/release_details.html", context)


@login_required
def add_to_wishlist(request, release_id: int):
    """
    Add a release to the authenticated user's wishlist or update it if
    already present.
    """
    release = get_object_or_404(Releases, pk=release_id)
    wishlist, _created = Wishlist.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = WishlistItemForm(request.POST)
        if form.is_valid():
            WishlistItem.objects.update_or_create(
                wishlist=wishlist,
                title=release,
                defaults={
                    'priority': form.cleaned_data['priority'],
                    'notes': form.cleaned_data['notes'],
                }
            )
            profile_url = reverse('user_profile')
            messages.success(
                request,
                mark_safe(
                    (
                        f'"{release.title}" added to your '
                        f'<a href="{profile_url}" class="no-underline">'
                        'wishlist</a>'
                    )
                )
            )
        else:
            messages.error(
                request,
                "There was a problem adding the item to your wishlist"
            )
    return redirect('release_details', release_id=release_id)


@superuser_required
def product_management(request):
    """
    List all releases and handle adding a new release.
    """
    releases = Releases.objects.all().order_by('id')
    if request.method == 'POST':
        form = ReleaseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Release added successfully")
            return redirect('product_management')
    else:
        form = ReleaseForm()
    return render(
        request,
        'releases/product_management.html',
        {
            'releases': releases,
            'form': form,
        }
    )


@superuser_required
def edit_release(request, release_id: int):
    """
    Edit an existing release.
    """
    release = get_object_or_404(Releases, pk=release_id)
    if request.method == 'POST':
        form = ReleaseForm(request.POST, request.FILES, instance=release)
        if form.is_valid():
            form.save()
            messages.success(request, "Release updated successfully")
            return redirect('product_management')
    else:
        form = ReleaseEditForm(instance=release)
    return render(
        request,
        'releases/edit_release.html',
        {
            'form': form,
            'release': release,
        }
    )


@superuser_required
def delete_release(request, release_id: int):
    """
    Delete a release after confirmation.
    """
    release = get_object_or_404(Releases, pk=release_id)
    if request.method == 'POST':
        release.delete()
        messages.success(request, "Release deleted successfully")
        return redirect('product_management')
    return render(
        request,
        'releases/delete_release.html',
        {'release': release}
    )


@superuser_required
def manage_images(request, release_id: int):
    """
    Manage images associated with a release.
    """
    release = get_object_or_404(Releases, pk=release_id)
    images = release.images.all()

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.title = release
            image.save()
            messages.success(request, "Image added successfully.")
            return redirect('manage_images', release_id=release.id)
    else:
        form = ImageForm()

    return render(request, 'releases/manage_images.html', {
        'release': release,
        'images': images,
        'form': form,
    })


@superuser_required
def delete_image(request, image_id: int):
    """
    Delete an image associated with a release.
    """
    image = get_object_or_404(Images, pk=image_id)
    release_id = image.title.id
    if request.method == 'POST':
        image.delete()
        messages.success(request, "Image deleted successfully")
    return redirect('manage_images', release_id=release_id)
