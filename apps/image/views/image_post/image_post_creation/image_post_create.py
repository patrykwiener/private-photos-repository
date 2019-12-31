from django.shortcuts import redirect
from django.urls import reverse_lazy

from apps.image.forms.image_post_create_form import ImagePostCreateForm
from apps.image.services.image_post_create_service import ImagePostCreateService
from apps.image.services.recognized_people_service import RecognizedPeopleService
from apps.image.views.image_post.image_post_creation.image_creation_base import ImageCreationBase


class ImagePostCreate(ImageCreationBase):
    form_class = ImagePostCreateForm
    template_name = 'image/image_post_create.html'
    success_url = reverse_lazy('image:image-post-list')
    upload_url = reverse_lazy("image:image-upload")

    def __init__(self):
        super().__init__()
        self._image_model = None

    def setup_form_view_attrs(self):
        self.initial = {
            'faces': self._image_model.facemodel_set.all(),
            'latitude': self._image_model.latitude,
            'longitude': self._image_model.longitude,
        }
        self.extra_context = {
            'object': self._image_model,
        }

    def get(self, request, *args, **kwargs):
        self._image_model = self.get_draft_if_exists().first()
        if not self._image_model:
            return redirect(self.upload_url)
        self.setup_form_view_attrs()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
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
        ImagePostCreateService(self._image_model, form.cleaned_data).execute()
        RecognizedPeopleService(self._image_model.facemodel_set.all(), form.cleaned_data).save_recognized_face()
        self.success_url = self._image_model.get_absolute_url()
        return super().form_valid(form)
