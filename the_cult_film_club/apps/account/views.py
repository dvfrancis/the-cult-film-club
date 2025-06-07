from django.shortcuts import render


def user_profile(request):
    """
    Display the user profile page
    """
    template = 'account/account.html'
    context = {}

    return render(request, template, context)