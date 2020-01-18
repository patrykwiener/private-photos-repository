from django import forms
from taggit.forms import TagField, TagWidget

from apps.image.models.image_model import ImageModel


class ImagePostCreateForm(forms.ModelForm):
    """
    Represents image post creation form.
    """

    class Meta:
        model = ImageModel
        fields = (
            'tags',
            'datetime_taken',
            'body',
            'latitude',
            'longitude',
        )

    def __init__(self, *args, **kwargs):
        """Initializes faces, latitude and longitude fields with the values given in **kwargs."""
        super().__init__(*args, **kwargs)
        initial = kwargs['initial']

        for face in initial['faces']:
            field_name = 'face_{}'.format(face.id)
            self.fields[field_name] = forms.CharField(max_length=100,
                                                      required=False,
                                                      initial=face.person.full_name if face.person else None,
                                                      widget=forms.TextInput(attrs={'autocomplete': 'off',
                                                                                    'spellcheck': 'false'}),
                                                      )

        self.fields['latitude'] = forms.DecimalField(max_digits=9,
                                                     decimal_places=6,
                                                     required=False,
                                                     initial=initial['latitude'])

        self.fields['longitude'] = forms.DecimalField(max_digits=9,
                                                      decimal_places=6,
                                                      required=False,
                                                      initial=initial['longitude'])

    body = forms.CharField(widget=forms.Textarea(), max_length=1024, required=False)

    datetime_taken = forms.DateTimeField(label='Date time taken', required=False,
                                         widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
                                         input_formats=['%Y-%m-%d %H:%M'])

    tags = TagField(required=False, widget=TagWidget(attrs={
        'class': 'form-control',
        'data-role': 'tagsinput',
    }))

    def get_faces(self):
        """
        Image face fields getter.

        :return: image face fields
        """
        return [field for field in self if 'face_' in field.name]
