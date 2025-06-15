from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from django.db.models import Q, Avg, F, Value
from the_cult_film_club.apps.releases.models import Releases, Rating, Images
from the_cult_film_club.apps.account.models import Wishlist, WishlistItem
from the_cult_film_club.apps.account.forms import WishlistItemForm
from django.core.paginator import Paginator
from django.db.models.functions import (
    Length, Substr, Reverse, StrIndex, ExtractYear
)
from .forms import ReleaseForm, ReleaseEditForm, ImageForm, RatingForm
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe


def releases(request):
    releases_list = Releases.objects.all()
    query = None
    sort = None
    direction = None

    # Filtering logic
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
        releases_list = releases_list.annotate(
            year=ExtractYear('release_date')
        ).filter(
            year__gte=int(decade),
            year__lt=int(decade) + 10
        )

    # For filter dropdowns, get unique genres and directors
    genres = (
        Releases.objects.values_list('genre', flat=True)
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

    # Get all years from releases for the decade filter dropdown
    years = (
        Releases.objects
        .annotate(year=ExtractYear('release_date'))
        .values_list('year', flat=True)
    )
    decades = sorted(set((y // 10) * 10 for y in years if y))

    # Search logic
    if 'q' in request.GET:
        query = request.GET['q']
        if not query:
            messages.error(
                request,
                "You didn't enter a search term. Please try again."
            )
            return redirect(reverse("home"))
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
        elif sort == 'copies_available':
            sortkey = 'copies_available'
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
        # Default to alphabetical sorting, by title, when no sort is specified
        releases_list = releases_list.order_by('title')

    paginator = Paginator(releases_list, 8)
    page_number = request.GET.get('page')
    releases = paginator.get_page(page_number)

    querydict = request.GET.copy()
    if 'page' in querydict:
        querydict.pop('page')
    querystring = querydict.urlencode()

    # For JavaScript filtering: get all unique combinations including decade
    all_filters = []
    for r in Releases.objects.values(
        "genre", "subgenre", "director", "release_date"
    ).distinct():
        year = r["release_date"].year if r["release_date"] else None
        decade_val = (year // 10) * 10 if year else None
        all_filters.append({
            "genre": r["genre"],
            "subgenre": r["subgenre"],
            "director": r["director"],
            "decade": decade_val,
        })

    context = {
        "releases": releases,
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


def release_details(request, release_id):
    release = get_object_or_404(Releases, pk=release_id)
    wishlist_form = WishlistItemForm()
    user_rating = None

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
    }
    return render(request, "releases/release_details.html", context)


def product_management(request):
    releases = Releases.objects.all().order_by('id')
    if request.method == 'POST':
        form = ReleaseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Release added successfully")
            return redirect('product_management')
    else:
        form = ReleaseForm()
    return render(request, 'releases/product_management.html', {
        'releases': releases,
        'form': form,
    })


def edit_release(request, release_id):
    release = get_object_or_404(Releases, id=release_id)
    if request.method == 'POST':
        form = ReleaseForm(request.POST, request.FILES, instance=release)
        if form.is_valid():
            form.save()
            messages.success(request, "Release updated successfully")
            return redirect('product_management')
    else:
        form = ReleaseEditForm(instance=release)
    return render(request, 'releases/edit_release.html', {
        'form': form,
        'release': release,
    })


def delete_release(request, release_id):
    release = get_object_or_404(Releases, id=release_id)
    if request.method == 'POST':
        release.delete()
        messages.success(request, "Release deleted successfully")
        return redirect('product_management')
    return render(request, 'releases/delete_release.html', {
        'release': release,
    })


def manage_images(request, release_id):
    release = get_object_or_404(Releases, id=release_id)
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


def delete_image(request, image_id):
    image = get_object_or_404(Images, id=image_id)
    release_id = image.title.id
    if request.method == 'POST':
        image.delete()
        messages.success(request, "Image deleted successfully")
    return redirect('manage_images', release_id=release_id)


@login_required
def add_to_wishlist(request, release_id):
    release = get_object_or_404(Releases, pk=release_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
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
