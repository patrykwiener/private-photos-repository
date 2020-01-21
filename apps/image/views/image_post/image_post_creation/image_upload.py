"""
This module contains ImageUpload class view responsible for uploading image file to the
system.
"""
from django.shortcuts import redirect
from django.urls import reverse_lazy

from apps.image.forms.image_upload_form import ImageUploadForm
from apps.image.services.image_processing.recognition import Recognition
from apps.image.services.image_upload_service import ImageUploadService
from apps.image.views.image_post.image_post_creation.image_creation_base import ImageCreationBase


class ImageUpload(ImageCreationBase):
    """Represents image upload view."""
    form_class = ImageUploadForm
    template_name = 'image/image_upload.html'
    success_url = reverse_lazy('image:image-post-create')

    def get(self, request, *args, **kwargs):
        """
        Handles GET request. Redirects when image post draft exists which means when the
        creation was not completed.
        """
        if self.get_draft_if_exists():
            return redirect(self.get_success_url())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handles GET request. Redirects when image post draft exists which means when the
        creation was not completed.
        """
        if self.get_draft_if_exists():
            return redirect(self.get_success_url())
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        """If form valid uploads image to the system and performs face recognition."""
        data = form.cleaned_data
        image_model = ImageUploadService(self.request.user, data['image']).upload()
        Recognition(image_model).execute()
        return super().form_valid(form)
