from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.utils.html import strip_tags
from .forms import ContactUsForm
import logging

logger = logging.getLogger(__name__)


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
            enquiry = form.save()

            # The enquiry is stored above and visible in the admin, so this
            # email is a notification rather than the record - without it an
            # enquiry can sit unread indefinitely. A failure is logged and does
            # not change what the visitor is told, because their message really
            # was received; an error would only prompt a duplicate submission.
            try:
                EmailMessage(
                    subject=(
                        "Cult Film Club enquiry from "
                        f"{enquiry.first_name} {enquiry.last_name}"
                    ),
                    # The message is a rich-text field, so the stored value is
                    # HTML. Strip it for a readable plain-text notification.
                    body=(
                        f"Name: {enquiry.first_name} {enquiry.last_name}\n"
                        f"Email: {enquiry.email}\n"
                        f"Received: {enquiry.created:%d %b %Y %H:%M}\n\n"
                        f"{strip_tags(enquiry.message)}"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[settings.DEFAULT_FROM_EMAIL],
                    reply_to=[enquiry.email],
                ).send()
            except Exception as e:
                logger.exception("Contact enquiry notification failed: %s", e)

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
