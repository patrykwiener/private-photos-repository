from django import forms


class ImageUploadForm(forms.Form):
    """
    Represents upload image form.
    """
    image = forms.ImageField(max_length=255)
