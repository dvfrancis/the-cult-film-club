from allauth.account.forms import SignupForm
from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from .models import Profile, Address, WishlistItem, PriorityLevel


class AccessibleCountrySelectWidget(CountrySelectWidget):
    """
    Custom CountrySelectWidget that removes invalid placeholder attribute
    and adds proper alt text to flag images
    """
    def __init__(self, attrs=None):
        # Remove placeholder from attrs if present
        if attrs and 'placeholder' in attrs:
            attrs = attrs.copy()
            del attrs['placeholder']
        super().__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)
        # Add alt attribute to the flag image
        html = html.replace(
            'src="/static/flags/__.gif"',
            'src="/static/flags/__.gif" alt="Country flag"'
        )
        return html


class AccountSignupForm(SignupForm):
    """
    Extends the default allauth SignupForm to collect additional user profile
    and address information during signup
    """

    photograph = forms.ImageField(
        required=False,
        label="Profile Photo",
        # Removes placeholder attribute from file input as it's not valid HTML
        widget=forms.ClearableFileInput()
    )
    first_line = forms.CharField(
        max_length=100, required=True,
        label="Address Line 1",
        widget=forms.TextInput(attrs={'placeholder': 'Address line 1'})
    )
    second_line = forms.CharField(
        max_length=100, required=False,
        label="Address Line 2",
        widget=forms.TextInput(attrs={'placeholder': 'Address line 2'})
    )
    city = forms.CharField(
        max_length=50, required=True,
        label="City",
        widget=forms.TextInput(attrs={'placeholder': 'City'})
    )
    county = forms.CharField(
        max_length=50, required=False,
        label="County",
        widget=forms.TextInput(attrs={'placeholder': 'County'})
    )
    postcode = forms.CharField(
        max_length=10, required=True,
        label="Postcode",
        widget=forms.TextInput(attrs={'placeholder': 'Postcode'})
    )
    country = CountryField().formfield(
        required=True,
        label="Country",
        # Uses custom widget that removes invalid placeholder
        widget=AccessibleCountrySelectWidget()
    )
    phone_number = forms.RegexField(
        regex=r'^\d+$',
        max_length=20,
        required=False,
        label="Phone Number",
        widget=forms.TextInput(attrs={
            'placeholder': 'Phone number',
            'pattern': '[0-9]*',
            'type': 'tel',
            'title': 'Numbers only (no spaces or symbols)'
        }),
        error_messages={
            'invalid': 'Enter a valid phone number (numbers only).'
        }
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add proper labels and attributes to inherited fields
        self.fields['email'].label = 'Email Address'
        self.fields['email'].widget.attrs.update(
            {'aria-label': 'Email Address'}
        )

        self.fields['email2'].label = 'Confirm Email Address'
        self.fields['email2'].widget.attrs.update(
            {'aria-label': 'Confirm Email Address'}
        )

        self.fields['username'].label = 'Username'
        self.fields['username'].widget.attrs.update({'aria-label': 'Username'})

        self.fields['password1'].label = 'Password'
        self.fields['password1'].widget.attrs.update(
            {'aria-label': 'Password'}
        )

        self.fields['password2'].label = 'Confirm Password'
        self.fields['password2'].widget.attrs.update(
            {'aria-label': 'Confirm Password'}
        )

        # Add aria-labels to custom fields
        self.fields['photograph'].widget.attrs.update(
            {'aria-label': 'Profile Photo'}
        )
        self.fields['first_line'].widget.attrs.update(
            {'aria-label': 'Address Line 1'}
        )
        self.fields['second_line'].widget.attrs.update(
            {'aria-label': 'Address Line 2'}
        )
        self.fields['city'].widget.attrs.update({'aria-label': 'City'})
        self.fields['county'].widget.attrs.update({'aria-label': 'County'})
        self.fields['postcode'].widget.attrs.update({'aria-label': 'Postcode'})
        self.fields['country'].widget.attrs.update({'aria-label': 'Country'})
        self.fields['phone_number'].widget.attrs.update(
            {'aria-label': 'Phone Number'}
        )

    def save(self, request):
        """
        Saves the user, their profile image, and creates an associated
        default address
        """
        user = super().save(request)
        profile = Profile.objects.get(user=user)

        # Save the uploaded photograph to the profile
        photograph = self.cleaned_data.get('photograph')
        if photograph:
            profile.photograph = photograph
        profile.save()

        # Create and link a new address as the default
        Address.objects.create(
            user=user,
            phone_number=self.cleaned_data.get('phone_number'),
            first_line=self.cleaned_data.get('first_line'),
            second_line=self.cleaned_data.get('second_line'),
            city=self.cleaned_data.get('city'),
            county=self.cleaned_data.get('county'),
            postcode=self.cleaned_data.get('postcode'),
            country=self.cleaned_data.get('country'),
            default_address=True
        )

        return user


class NoClearableFileInput(forms.ClearableFileInput):
    """
    A custom ClearableFileInput widget that removes the 'clear' checkbox
    """
    template_name = 'widgets/no_clearable_file_input.html'


class ProfilePhotoForm(forms.ModelForm):
    """
    A form for updating a user's profile photograph.
    """

    class Meta:
        model = Profile
        fields = ['photograph']
        widgets = {
            'photograph': NoClearableFileInput,
        }


class AddressForm(forms.ModelForm):
    """
    A form for creating or editing a user address
    The user field is excluded and should be set in the view
    """

    class Meta:
        model = Address
        fields = [
            'label', 'first_line', 'second_line', 'city', 'county',
            'postcode', 'country', 'phone_number', 'default_address'
        ]
        widgets = {
            'label': forms.TextInput(attrs={'placeholder': 'Address Label'}),
            'first_line': forms.TextInput(
                attrs={'placeholder': 'Address Line 1'}
            ),
            'second_line': forms.TextInput(
                attrs={'placeholder': 'Address Line 2'}
            ),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'county': forms.TextInput(attrs={'placeholder': 'County'}),
            'postcode': forms.TextInput(attrs={'placeholder': 'Postcode'}),
            # Uses custom widget that removes invalid placeholder
            'country': AccessibleCountrySelectWidget(),
            'phone_number': forms.TextInput(
                attrs={'placeholder': 'Phone number'}
            ),
        }
        exclude = ['user']


class WishlistItemForm(forms.ModelForm):
    """
    A form for adding or editing items in the user's wishlist
    """

    class Meta:
        model = WishlistItem
        fields = ['title', 'notes', 'priority']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2}),
            'priority': forms.Select(
                choices=[(tag.value, tag.value) for tag in PriorityLevel]
            ),
        }
