from allauth.account.forms import SignupForm
from django import forms
from .models import Profile, Address
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


class AccountSignupForm(SignupForm):
    photograph = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'placeholder': 'Profile photo'})
    )
    first_line = forms.CharField(
        max_length=100, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Address line 1'})
    )
    second_line = forms.CharField(
        max_length=100, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Address line 2'})
    )
    city = forms.CharField(
        max_length=50, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'City'})
    )
    county = forms.CharField(
        max_length=50, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'County'})
    )
    postcode = forms.CharField(
        max_length=10, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Postcode'})
    )
    country = CountryField().formfield(
        required=False,
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


class ProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photograph']


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['user']  # user will be set in the view
