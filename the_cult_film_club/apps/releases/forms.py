from django import forms
from .models import Releases, Images, Rating
from django_ckeditor_5.widgets import CKEditor5Widget
from django.forms.widgets import ClearableFileInput


class CustomClearableFileInput(ClearableFileInput):
    template_name = 'django/forms/widgets/clearable_file_input.html'

    def format_value(self, value):
        if self.is_initial(value):
            return value
        return None

    def value_from_datadict(self, data, files, name):
        upload = super().value_from_datadict(data, files, name)
        if not self.is_required and self.clear_checkbox_name(name) in data:
            if upload:
                return upload
            return False
        return upload


class ReleaseForm(forms.ModelForm):
    """
    Form for creating or adding new Releases with selected fields.
    Uses CKEditor5Widget for rich text fields.
    """
    class Meta:
        model = Releases
        fields = [
            'title', 'release_date', 'director', 'description', 'genre',
            'subgenre', 'resolution', 'special_features', 'edition',
            'censor_status', 'packaging', 'copies_available', 'price'
        ]
        widgets = {
            'description': CKEditor5Widget(config_name="extends"),
            'special_features': CKEditor5Widget(config_name="extends"),
            'release_date': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
            'price': forms.NumberInput(attrs={'step': '0.01', 'min': 0}),
            'copies_available': forms.NumberInput(attrs={'min': 0}),
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
            'price': 'Price',
        }
        help_texts = {
            'title': 'Enter the title of the release.',
            'release_date': 'Select the release date.',
            'copies_available': 'Enter the number of copies available.',
            'price': 'Set the price for this release.',
        }
        error_messages = {
            'title': {
                'required': 'This field is required.',
                'max_length': 'Title cannot exceed 100 characters.'
            },
            'release_date': {
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['release_date'].input_formats = ['%Y-%m-%d']


class ImageForm(forms.ModelForm):
    """
    Form for adding or editing images related to a release.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add custom attributes to the image field
        self.fields['image'].widget.attrs.update({
            'class': 'form-control',
            'aria-label': 'Select image file'
        })

    class Meta:
        model = Images
        fields = ['image', 'caption', 'is_featured']
        widgets = {
            'image': CustomClearableFileInput(),
        }
        labels = {
            'image': 'Image',
            'caption': 'Caption',
            'is_featured': 'Featured Image',
        }
        help_texts = {
            'caption': 'Enter a descriptive caption for the image.',
            'is_featured': 'Check this box to make this the featured image.',
        }


class ReleaseEditForm(forms.ModelForm):
    """
    Full edit form for Releases, including all fields.
    Uses CKEditor5Widget for rich text fields.
    Intended for admin or advanced editing.
    """
    class Meta:
        model = Releases
        fields = "__all__"
        widgets = {
            "description": CKEditor5Widget(config_name="extends"),
            "special_features": CKEditor5Widget(config_name="extends"),
            'release_date': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
            'price': forms.NumberInput(attrs={'step': '0.01', 'min': 0}),
            'copies_available': forms.NumberInput(attrs={'min': 0}),
        }


class RatingForm(forms.ModelForm):
    """
    Form for users to submit or update ratings and reviews.
    """
    class Meta:
        model = Rating
        fields = ['rating', 'review']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'review': CKEditor5Widget(config_name="extends"),
        }
        labels = {
            'rating': 'Rating (1 to 5)',
            'review': 'Review',
        }
        help_texts = {
            'rating': 'Provide a rating between 1 and 5.',
        }
