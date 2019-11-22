from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic.edit import FormView

from apps.image.forms import ImageUploadForm, CreateImagePostFacesForm
from apps.image.models.face_model import FaceModel
from apps.image.models.image_model import ImageModel
from apps.image.services.create_image_post import CreateImagePost
from apps.image.services.image_processing.recognition import Recognition
from apps.image.services.upload_image import UploadImage


class UploadImageBase:
    @staticmethod
    def get_draft_if_exists():
        return ImageModel.objects.filter(status=ImageModel.DRAFT)


class UploadImageView(UploadImageBase, FormView):
    form_class = ImageUploadForm
    template_name = 'image/upload.html'
    success_url = '/image/create-image-post'

    def dispatch(self, request, *args, **kwargs):
        if self.get_draft_if_exists():
            return redirect(self.get_success_url())
        return super(UploadImageView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        data = form.cleaned_data
        image_model = UploadImage(data).create_draft()
        Recognition(image_model).execute()
        return super(UploadImageView, self).form_valid(form)


class CreateImagePostView(UploadImageBase, FormView):
    form_class = CreateImagePostFacesForm
    template_name = 'image/create_image_post.html'
    success_url = '/image/upload-image'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._image_model = None
        self._faces = None

    def obtain_context_attrs(self):
        self._image_model = self.get_draft_if_exists().first()
        self._faces = FaceModel.objects.filter(image=self._image_model)

    def setup_form_view_attrs(self):
        self.initial = {
            'faces': self._faces,
            'latitude': self._image_model.latitude,
            'longitude': self._image_model.longitude,
        }
        self.extra_context = {
            'faces': self._faces,
            'thumb': self._image_model.thumbnail,
            'date_time_taken': self._image_model.date_time_taken,
        }

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.obtain_context_attrs()

    def dispatch(self, request, *args, **kwargs):
        if not self._image_model:
            return redirect(self.get_success_url())
        self.setup_form_view_attrs()
        return super(CreateImagePostView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'cancel' in request.POST:
            self._image_model.delete()
            return redirect(self.get_success_url())
        elif 'upload' in request.POST:
            post_result = super(CreateImagePostView, self).post(request, *args, **kwargs)
            return post_result

    def form_valid(self, form):
        CreateImagePost(self._image_model, self._faces, form.cleaned_data).execute()
        messages.success(self.request, 'The post has been created!')
        return super(CreateImagePostView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Oops! Something went wrong. Check your inputs!')
        return super(CreateImagePostView, self).form_invalid(form)
