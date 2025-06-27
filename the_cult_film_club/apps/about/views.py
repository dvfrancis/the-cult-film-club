from django.shortcuts import render


def about(request):
    """
    Render the About page
    """
    return render(request, "about/about.html")
