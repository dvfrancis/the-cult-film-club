from django import forms
from django.utils import timezone
from .models import Order, DiscountCode
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


class AccessibleCountrySelectWidget(CountrySelectWidget):
    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs['class'] = 'form-control countryselectwidget form-select'

    def create_option(
        self, name, value, label, selected, index,
        subindex=None, attrs=None
    ):
        option = super().create_option(
            name, value, label, selected, index, subindex, attrs
        )
        return option

    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)
        # Add alt text to flag image
        html = html.replace(
            '<img class="country-select-flag"',
            '<img class="country-select-flag" alt="Country flag"'
        )
        return html


class OrderForm(forms.ModelForm):
    """
    Accessible order form with visible labels, placeholders,
    required field indicators, and custom styling.
    """

    country = CountryField().formfield(
        required=True,
        widget=AccessibleCountrySelectWidget(
            attrs={'class': 'form-control', 'required': True}
        ),
        label="Country"
    )

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
        }

    def __init__(self, *args, **kwargs):
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
                continue  # Country widget handled above

            placeholder = placeholders.get(field_name, '')
            if field.required:
                placeholder += ' *'

            field.widget.attrs.update({
                'placeholder': placeholder,
                'class': 'stripe-style-input form-control',
            })


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
