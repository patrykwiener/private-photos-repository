from django import forms


class ImageUploadForm(forms.Form):
    image = forms.ImageField(max_length=255)
