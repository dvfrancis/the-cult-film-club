from django import forms
from .models import ContactUs


class ContactUsForm(forms.ModelForm):
    """
    Form for users to submit contact messages.
    Uses the ContactUs model fields: first name, last name, email, and message.
    """

    class Meta:
        model = ContactUs
        fields = ['first_name', 'last_name', 'email', 'message']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Your first name',
                'class': 'form-control',
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Your last name',
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Your email address',
                'class': 'form-control',
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Write your message here...',
                'class': 'form-control',
                'rows': 5,
            }),
        }
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
            'message': 'Message',
        }
