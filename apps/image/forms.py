from typing import List
from django import forms
from apps.image.models.face_model import FaceModel


class ImageUploadForm(forms.Form):
    image = forms.ImageField(max_length=255)


class CreateImagePostForm(forms.Form):

    def __init__(self, *args, **kwargs):
        faces = kwargs.pop('faces')  # type: List[FaceModel]
        super(CreateImagePostForm, self).__init__(*args, **kwargs)
        for face in faces:
            field_name = 'face_{}'.format(face.id)
            self.fields[field_name] = forms.CharField(max_length=100,
                                                      required=False,
                                                      initial=face.person.full_name if face.person else None,
                                                      widget=forms.TextInput(attrs={'autocomplete': 'off',
                                                                                    'spellcheck': 'false'}),
                                                      )
