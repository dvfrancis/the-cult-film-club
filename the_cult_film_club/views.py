from django.shortcuts import render
from django.http import HttpResponseBadRequest
from django.core.exceptions import PermissionDenied


def page_not_found(request, exception=None):
    """
    Render the custom 404 error page.

    This view handles 'page not found' errors, and renders a custom 404 error
    page.

    Args:
        request: The HTTP request object.
        exception: The exception that triggered the 404 error (optional).

    Returns:
        HttpResponse: The rendered 404 error page with a 404 status code.
    """
    return render(request, 'error_pages/page_not_found.html', status=404)


def server_error(request):
    """
    Render the custom 500 error page.

    This view handles server errors, and renders a custom 500 error page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered 500 error page with a 500 status code.
    """
    return render(request, "error_pages/server_error.html", status=500)


def custom_permission_denied(request, exception=None):
    """
    Render the custom 403 error page.

    This view handles permission denied errors, and renders a custom 403 error
    page.

    Args:
        request: The HTTP request object.
        exception: The exception that triggered the 403 error (optional).

    Returns:
        HttpResponse: The rendered 403 error page with a 403 status code.
    """
    return render(request, "error_pages/permission_denied.html", status=403)


def bad_request(request, exception=None):
    """
    Render the custom 400 error page.

    This view handles bad request errors, and renders a custom 400 error page.
    
    Args:
        request: The HTTP request object.
        exception: The exception that triggered the 400 error (optional).
    Returns:
        HttpResponse: The rendered 400 error page with a 400 status code.
    """
    return render(request, "error_pages/bad_request.html", status=400)










