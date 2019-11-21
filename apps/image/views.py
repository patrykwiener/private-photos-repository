from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic.edit import FormView

from apps.image.forms import ImageUploadForm, CreateImagePostForm
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
        image = form.cleaned_data['image']
        image_model = UploadImage(image).create_draft()
        Recognition(image_model).execute()
        return super(UploadImageView, self).form_valid(form)


class CreateImagePostView(UploadImageBase, FormView):
    form_class = CreateImagePostForm
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
            'faces': self._faces
        }
        self.extra_context = {
            'faces': self._faces,
            'thumb': self._image_model.thumbnail
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
            messages.success(request, 'The post has been created!')
            return post_result

    def form_valid(self, form):
        for face in self._faces:
            field_name = 'face_{}'.format(face.id)
            face_name = form.cleaned_data[field_name]
            CreateImagePost.save_recognized_face(face, face_name)
        CreateImagePost.publish(self._image_model)
        return super(CreateImagePostView, self).form_valid(form)
