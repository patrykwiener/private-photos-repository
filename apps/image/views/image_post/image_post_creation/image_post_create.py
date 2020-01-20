"""This module contains ImagePostCreate class view responsible for image post creation."""
from django.shortcuts import redirect
from django.urls import reverse_lazy

from apps.image.forms.image_post_create_form import ImagePostCreateForm
from apps.image.services.image_post_create_service import ImagePostCreateService
from apps.image.services.recognized_people_service import RecognizedPeopleService
from apps.image.views.image_post.image_post_creation.image_creation_base import ImageCreationBase


class ImagePostCreate(ImageCreationBase):
    """Represents image post creation view."""
    form_class = ImagePostCreateForm
    template_name = 'image/image_post_create.html'
    success_url = reverse_lazy('image:image-post-list')
    upload_url = reverse_lazy("image:image-upload")

    def __init__(self):
        super().__init__()
        self._image_model = None

    def setup_form_view_attrs(self):
        """
        Sets up initial form values such as faces on an image and image taken coordinates. Also
        adds ImageModel object to context.
        """
        self.initial = {
            'faces': self._image_model.facemodel_set.all(),
            'latitude': self._image_model.latitude,
            'longitude': self._image_model.longitude,
        }
        self.extra_context = {
            'object': self._image_model,
        }

    def get(self, request, *args, **kwargs):
        """
        Handles GET request. Redirects to ImageUpload view when user's ImageModel with DRAFT
        status does not exists. Sets up form arguments.
        """
        self._image_model = self.get_draft_if_exists().first()
        if not self._image_model:
            return redirect(self.upload_url)
        self.setup_form_view_attrs()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handles POST request. Redirects to ImageUpload view when user's ImageModel with DRAFT
        status does not exists. Sets up form arguments. Deletes image post and redirects when
        'cancel' is in request. Performs form checking on 'upload' in request object.
        """
        self._image_model = self.get_draft_if_exists().first()
        if not self._image_model:
            return redirect(self.upload_url)
        self.setup_form_view_attrs()
        if 'cancel' in request.POST:
            self._image_model.delete()
            return redirect(self.upload_url)
        elif 'upload' in request.POST:
            return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        """
        If form valid fills ImageModel object with values given in form. Changes ImagePost status
        to PUBLISHED. Updates recognized faces.
        """
        ImagePostCreateService(self._image_model, form.cleaned_data).execute()
        RecognizedPeopleService(self._image_model.facemodel_set.all(),
                                form.cleaned_data).save_recognized_face()
        self.success_url = self._image_model.get_absolute_url()
        return super().form_valid(form)
