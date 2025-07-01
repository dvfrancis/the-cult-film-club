from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail

from .forms import NewsletterSignupForm
from .models import NewsletterSignup


def newsletter_signup(request):
    """
    Handle newsletter subscription form rendering and submission.
    If the user is authenticated, their current subscription is checked.
    """
    subscriber = None
    if request.user.is_authenticated:
        subscriber = (
            NewsletterSignup.objects
            .filter(email=request.user.email)
            .first()
        )

    if request.method == 'POST':
        form = NewsletterSignupForm(request.POST, instance=subscriber)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                (
                    "Thanks! You've been subscribed to The Cult Film Club "
                    "newsletter."
                )
            )
            return redirect('newsletter_signup')
    else:
        # Pass subscriber instance so the form shows current data
        form = NewsletterSignupForm(instance=subscriber)

    context = {
        'form': form,
        'subscriber': subscriber
    }

    return render(request, 'newsletter/newsletter.html', context)


def edit_newsletter_preferences(request, token):
    subscriber = get_object_or_404(NewsletterSignup, unsubscribe_token=token)

    if request.method == 'POST':
        form = NewsletterSignupForm(request.POST, instance=subscriber)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Your newsletter preferences have been updated."
            )
            return redirect('newsletter_signup')
    else:
        form = NewsletterSignupForm(instance=subscriber)

    return render(
        request,
        'newsletter/edit_newsletter_preferences.html',
        {'form': form}
    )


def unsubscribe(request, token):
    """
    Handle unsubscribe confirmation and removal via tokenized URL.
    GET: Show unsubscribe confirmation form.
    POST: Unsubscribe the user and delete the subscription.
    """
    subscriber = get_object_or_404(NewsletterSignup, unsubscribe_token=token)

    if request.method == "POST":
        subscriber.delete()
        messages.success(
            request,
            "You have been unsubscribed from The Cult Film Club newsletter."
        )
        return redirect('home')

    return render(
        request,
        "newsletter/unsubscribe.html",
        {"subscriber": subscriber}
    )


def newsletter_unsubscribe_request(request):
    """
    Handle unsubscribe link request:
    - User submits their email.
    - If subscribed, an email with unsubscribe link is sent.
    """
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        subscriber = NewsletterSignup.objects.filter(email=email).first()

        if subscriber and subscriber.unsubscribe_token:
            # Generate full unsubscribe URL
            unsubscribe_url = request.build_absolute_uri(
                reverse(
                    'newsletter_unsubscribe',
                    args=[subscriber.unsubscribe_token]
                )
            )

            # Send unsubscribe email
            send_mail(
                subject="Unsubscribe from The Cult Film Club Newsletter",
                message=f"Click here to unsubscribe: {unsubscribe_url}",
                from_email="tcfc@dominicfrancis.co.uk",
                recipient_list=[email],
            )

            messages.success(
                request,
                "Check your email for an unsubscribe link."
            )
        else:
            messages.error(request, "Email not found.")

    return redirect('newsletter_signup')
