from django import forms
from django.utils import timezone
from .models import Order, DiscountCode


class OrderForm(forms.ModelForm):
    """
    Form for capturing order information.
    Customizes field placeholders, CSS classes,
    removes labels, and sets autofocus on full_name.
    """
    class Meta:
        model = Order
        fields = (
            'full_name', 'email', 'phone_number',
            'street_address1', 'street_address2',
            'town_or_city', 'postcode', 'country',
            'county',
        )
        widgets = {
            'full_name': forms.TextInput(attrs={'required': True}),
            'email': forms.EmailInput(attrs={'required': True}),
            'street_address1': forms.TextInput(attrs={'required': True}),
            'town_or_city': forms.TextInput(attrs={'required': True}),
            'postcode': forms.TextInput(attrs={'required': True}),
            'country': forms.Select(attrs={'required': True}),
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize form fields with placeholders, CSS classes,
        remove labels, and set autofocus on full_name field.
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field_name, field in self.fields.items():
            if field_name == 'country':
                continue  # Skip country field placeholder to use default
            placeholder_text = placeholders.get(field_name, '')
            if field.required:
                placeholder_text += ' *'
            field.widget.attrs.update({
                'placeholder': placeholder_text,
                'class': 'stripe-style-input',
            })
            field.label = False


class DiscountCodeForm(forms.ModelForm):
    """
    Form for managing DiscountCode instances with
    date pickers for valid_from and valid_to.
    """
    class Meta:
        model = DiscountCode
        fields = ['code', 'percent', 'valid_from', 'valid_to', 'is_active']
        widgets = {
            'valid_from': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
            'valid_to': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
        }

    def __init__(self, *args, **kwargs):
        """
        Ensure date input formats are consistent and set min date for
        frontend validation.
        """
        super().__init__(*args, **kwargs)
        today = timezone.now().date().isoformat()
        for field_name in ['valid_from', 'valid_to']:
            self.fields[field_name].input_formats = ['%Y-%m-%d']
            self.fields[field_name].widget.attrs['min'] = today

    def clean(self):
        cleaned_data = super().clean()
        valid_from = cleaned_data.get('valid_from')
        valid_to = cleaned_data.get('valid_to')
        today = timezone.now().date()

        if valid_from and valid_from < today:
            self.add_error(
                'valid_from',
                "The start date cannot be in the past"
            )
        if valid_to and valid_to < today:
            self.add_error('valid_to', "The end date cannot be in the past")
        if valid_from and valid_to and valid_to < valid_from:
            self.add_error(
                'valid_to',
                "The end date cannot be before the start date"
            )
