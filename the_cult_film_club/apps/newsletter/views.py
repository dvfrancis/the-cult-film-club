from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from .forms import NewsletterSignupForm
from .models import NewsletterSignup
from django.core.mail import send_mail


def newsletter_signup(request):
    signup = None
    if request.user.is_authenticated:
        signup = (
            NewsletterSignup.objects.filter(email=request.user.email).first()
        )

    if request.method == 'POST':
        form = NewsletterSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                (
                    "Thanks! You've been subscribed to The Cult Film Club "
                    "newsletter"
                )
            )
            return redirect('newsletter_signup')
    else:
        form = NewsletterSignupForm()

    return render(
        request,
        'newsletter/newsletter.html',
        {'form': form, 'subscriber': signup}
    )


def unsubscribe(request, token):
    subscriber = get_object_or_404(NewsletterSignup, unsubscribe_token=token)
    if request.method == "POST":
        subscriber.delete()
        messages.success(
            request,
            "You have been unsubscribed from The Cult Film Club newsletter"
        )
        return redirect('home')
    return render(
        request,
        "newsletter/unsubscribe.html",
        {"subscriber": subscriber}
    )


def newsletter_unsubscribe_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        subscriber = NewsletterSignup.objects.filter(email=email).first()
        if subscriber and subscriber.unsubscribe_token:
            unsubscribe_url = request.build_absolute_uri(
                reverse(
                    'newsletter_unsubscribe',
                    args=[subscriber.unsubscribe_token]
                )
            )
            send_mail(
                "Unsubscribe from The Cult Film Club Newsletter",
                f"Click here to unsubscribe: {unsubscribe_url}",
                "tcfc@dominicfrancis.co.uk",
                [email],
            )
            messages.success(
                request,
                "Check your email for an unsubscribe link"
            )
        else:
            messages.error(request, "Email not found.")
    return redirect('newsletter_signup')
