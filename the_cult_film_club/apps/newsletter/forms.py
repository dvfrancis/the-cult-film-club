from django import forms
from .models import NewsletterSignup
from the_cult_film_club.apps.releases.models import Releases


def get_genre_choices():
    genres = (
        Releases.objects
        .exclude(genre__isnull=True)
        .exclude(genre__exact="")
        .values_list('genre', flat=True)
        .distinct()
    )
    return [(g, g) for g in genres]


class NewsletterSignupForm(forms.ModelForm):
    genres = forms.MultipleChoiceField(
        choices=[],
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="I am interested in the following topics:"
    )

    class Meta:
        model = NewsletterSignup
        fields = ['email', 'genres']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['genres'].choices = get_genre_choices()

    def clean_genres(self):
        # Store as comma-separated string
        return ",".join(self.cleaned_data['genres'])
