from allauth.account.forms import SignupForm
from django import forms
from .models import Profile, Address, WishlistItem, PriorityLevel
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


class AccountSignupForm(SignupForm):
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
    phone_number = forms.CharField(
        max_length=20, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Phone number'})
    )

    def save(self, request):
        user = super().save(request)
        profile = Profile.objects.get(user=user)
        # Save the uploaded photograph to CloudinaryField
        photograph = self.cleaned_data.get('photograph')
        if photograph:
            profile.photograph = photograph
        profile.save()
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
        profile.address.add(address)
        return user


class NoClearableFileInput(forms.ClearableFileInput):
    template_name = 'widgets/no_clearable_file_input.html'


class ProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photograph']
        widgets = {
            'photograph': NoClearableFileInput,
        }


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'label', 'first_line', 'second_line', 'city', 'county',
            'postcode', 'phone_number', 'default_address'
        ]
        widgets = {
            'label': forms.TextInput(
                attrs={'placeholder': 'Address Label'}
            ),
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
        exclude = ['user']  # user will be set in the view


class WishlistItemForm(forms.ModelForm):
    class Meta:
        model = WishlistItem
        fields = ['title', 'notes', 'priority']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2}),
            'priority': forms.Select(
                choices=[(tag.value, tag.value) for tag in PriorityLevel]
            ),
        }
