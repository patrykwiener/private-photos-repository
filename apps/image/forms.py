from django import forms


class ImageUploadForm(forms.Form):
    image = forms.ImageField(max_length=255)


class CreateImagePostFacesForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(CreateImagePostFacesForm, self).__init__(*args, **kwargs)
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
    date_taken = forms.DateField(required=True)

    def get_faces(self):
        return [field for field in self if 'face_' in field.name]
