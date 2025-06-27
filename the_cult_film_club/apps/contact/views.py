from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactUsForm


def contact_us(request):
    """
    Handle the Contact Us form submission.

    - On GET request, display an empty contact form.
    - On POST request, validate and save the form.
      If valid, save the submission, show success message,
      and redirect to avoid form resubmission.
    - If the form is invalid, re-render the form with errors.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered template with form context.
    """
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            # Save the valid form data to the database
            form.save()

            # Add a success message to be displayed to the user
            messages.success(
                request,
                "Thank you for contacting us! We'll respond as soon as we can."
            )

            # Redirect after POST to prevent duplicate submissions on refresh
            return redirect('contact_us')
        else:
            # Optional: Add an error message or just render the form
            # with errors
            messages.error(request, "Please correct the errors below.")
    else:
        # Create a blank form instance for GET requests
        form = ContactUsForm()

    # Render the contact form template with the form instance
    return render(request, 'contact/contact_us.html', {'form': form})
