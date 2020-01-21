"""This module contains ImagePostShareForm class representing image post share form."""
from django import forms

from apps.image.models.shared_image_model import SharedImageModel
from apps.users.models import CustomUser


class ImagePostShareForm(forms.Form):
    """Represents image post share form."""

    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.get('initial').get('user')
        self.image = kwargs.get('initial').get('image')
        super().__init__(*args, **kwargs)

    def clean_email(self):
        """
        Cleans email filed and validates correctness of the provided email.

        @:raises: ValidationError, when user with the given email does not exist or
                    user tries to share image with himself or
                    the image has been already shared with the email owner.
        :return: provided email
        """
        email = self.cleaned_data.get('email')
        if not CustomUser.objects.filter(email=email).count():
            raise forms.ValidationError('User with the given email does not exist.')
        if self.user and self.user.email == email:
            raise forms.ValidationError('You cannot share an image with yourself.')
        if SharedImageModel.objects.filter(recipient=CustomUser.objects.get(email=email), image=self.image).count():
            raise forms.ValidationError('You\'re already sharing this image with the given user.')
        return email
