from django import forms
from .models import Releases, Images
from django_ckeditor_5.widgets import CKEditor5Widget


class ReleaseForm(forms.ModelForm):
    class Meta:
        model = Releases
        fields = [
            'title', 'release_date', 'director', 'description', 'genre',
            'subgenre', 'resolution', 'special_features', 'edition',
            'censor_status', 'packaging', 'copies_available', 'price'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'special_features': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'title': 'Title',
            'release_date': 'Release Date',
            'director': 'Director',
            'description': 'Description',
            'genre': 'Genre',
            'subgenre': 'Subgenre',
            'resolution': 'Resolution',
            'special_features': 'Special Features',
            'edition': 'Edition',
            'censor_status': 'Censor Status',
            'packaging': 'Packaging',
            'copies_available': 'Copies Available',
            'price': 'Price'
        }
        help_texts = {
            'title': 'Enter the title of the release.',
            'release_date': 'Select the release date.',
            'director': 'Enter the director\'s name.',
            'description': 'Provide a brief description of the release.',
            'genre': 'Specify the genre of the release.',
            'subgenre': 'Specify the subgenre of the release.',
            'resolution': 'Enter the resolution (for example, 1080p, 4K).',
            'special_features': 'List any special features included.',
            'edition': (
                'Specify the edition (for example, Collector\'s Edition).'
            ),
            'censor_status': 'Enter the censor status if applicable.',
            'packaging': 'Describe the packaging type.',
            'copies_available': 'Enter the number of copies available.',
            'price': 'Set the price for this release.'
        }
        error_messages = {
            'title': {
                'required': 'This field is required.',
                'max_length': 'Title cannot exceed 100 characters.'
            },
            'release_date': {
                'required': 'This field is required.'
            },
            'director': {
                'required': 'This field is required.'
            },
            'description': {
                'required': 'This field is required.'
            },
            'genre': {
                'required': 'This field is required.'
            },
            'subgenre': {
                'required': 'This field is required.'
            },
            'resolution': {
                'required': 'This field is required.'
            },
            'special_features': {
                'required': 'This field is required.'
            },
            'edition': {
                'required': 'This field is required.'
            },
            'censor_status': {
                'required': 'This field is required.'
            },
            'packaging': {
                'required': 'This field is required.'
            },
            'copies_available': {
                'required': 'This field is required.',
                'invalid': 'Enter a valid number of copies.'
            },
            'price': {
                'required': 'This field is required.',
                'invalid': 'Enter a valid price.'
            }
        }
        widgets.update({
            'release_date': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
            'copies_available': forms.NumberInput(attrs={'min': 0}),
        })

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['release_date'].input_formats = ['%Y-%m-%d']


class ImageForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ['image', 'caption', 'is_featured']


class ReleaseEditForm(forms.ModelForm):
    class Meta:
        model = Releases
        fields = "__all__"
        widgets = {
            "description": CKEditor5Widget(config_name="extends"),
            "special_features": CKEditor5Widget(config_name="extends"),
        }
