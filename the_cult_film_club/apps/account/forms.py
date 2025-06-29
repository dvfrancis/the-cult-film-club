from allauth.account.forms import SignupForm
from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from .models import Profile, Address, WishlistItem, PriorityLevel


class AccountSignupForm(SignupForm):
    """
    Extends the default allauth SignupForm to collect additional user profile
    and address information during signup
    """

    photograph = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'placeholder': 'Profile photo'})
    )
    first_line = forms.CharField(
        max_length=100, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Address line 1'})
    )
    second_line = forms.CharField(
        max_length=100, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Address line 2'})
    )
    city = forms.CharField(
        max_length=50, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'City'})
    )
    county = forms.CharField(
        max_length=50, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'County'})
    )
    postcode = forms.CharField(
        max_length=10, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Postcode'})
    )
    country = CountryField().formfield(
        required=True,
        widget=CountrySelectWidget(attrs={'placeholder': 'Country'})
    )
    phone_number = forms.RegexField(
        regex=r'^\d+$',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Phone number',
            'inputmode': 'numeric',
            'pattern': '[0-9]*',
            'type': 'tel',
            'title': 'Numbers only (no spaces or symbols)'
        }),
        error_messages={
            'invalid': 'Enter a valid phone number (numbers only).'
        }
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
        address = Address.objects.create(
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
            'postcode', 'phone_number', 'default_address'
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
