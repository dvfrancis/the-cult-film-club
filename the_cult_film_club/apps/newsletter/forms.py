from django import forms
from .models import NewsletterSignup
from the_cult_film_club.apps.releases.models import Releases


def get_genre_choices():
    """
    Return a list of distinct non-empty genre values from Releases
    for use in the newsletter signup form.
    """
    genres = (
        Releases.objects
        .exclude(genre__isnull=True)
        .exclude(genre__exact="")
        .values_list('genre', flat=True)
        .distinct()
    )
    return [(genre, genre) for genre in genres]


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
        """
        Dynamically assign genre choices based on current releases.
        """
        super().__init__(*args, **kwargs)
        self.fields['genres'].choices = get_genre_choices()

        # When editing, convert comma string to list for the field initial data
        if self.instance and self.instance.genres:
            self.initial['genres'] = self.instance.genres.split(',')

    def clean_genres(self):
        """
        Join selected genres into a comma-separated string before saving.
        """
        return ",".join(self.cleaned_data.get('genres', []))
