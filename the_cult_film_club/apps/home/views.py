from django.shortcuts import render


def index(request):
    """
    Render the home page of the Cult Film Club.
    """
    return render(request, 'home/index.html')
