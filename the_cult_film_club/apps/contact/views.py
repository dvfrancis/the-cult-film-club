from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactUsForm


def contact_us(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Thank you for contacting us! We'll respond as soon as we can."
            )
            return redirect('contact_us')
    else:
        form = ContactUsForm()
    return render(request, 'contact/contact_us.html', {'form': form})
