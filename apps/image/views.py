from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView, UpdateView, DeleteView

from apps.image.forms import ImageUploadForm, CreateImagePostForm
from apps.image.models.image_model import ImageModel
from apps.image.services.create_image_post import CreateImagePost
from apps.image.services.create_people import CreatePeople
from apps.image.services.image_processing.recognition import Recognition
from apps.image.services.upload_image import UploadImage


class UploadImageBase(FormView):
    @staticmethod
    def get_draft_if_exists():
        return ImageModel.objects.filter(status=ImageModel.DRAFT)


class UploadImageView(UploadImageBase):
    form_class = ImageUploadForm
    template_name = 'image/image_upload.html'
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


class CreateImagePostView(UploadImageBase):
    form_class = CreateImagePostForm
    template_name = 'image/image_post_create.html'
    upload_url = '/image/upload-image'
    success_url = '/'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._image_model = None

    def obtain_context_attrs(self):
        self._image_model = self.get_draft_if_exists().first()

    def setup_form_view_attrs(self):
        self.initial = {
            'faces': self._image_model.facemodel_set.all(),
            'latitude': self._image_model.latitude,
            'longitude': self._image_model.longitude,
        }
        self.extra_context = {
            'object': self._image_model,
        }

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.obtain_context_attrs()

    def dispatch(self, request, *args, **kwargs):
        if not self._image_model:
            return redirect(self.upload_url)
        self.setup_form_view_attrs()
        return super(CreateImagePostView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'cancel' in request.POST:
            self._image_model.delete()
            return redirect(self.upload_url)
        elif 'upload' in request.POST:
            post_result = super(CreateImagePostView, self).post(request, *args, **kwargs)
            return post_result

    def form_valid(self, form):
        CreateImagePost(self._image_model, form.cleaned_data).execute()
        CreatePeople(self._image_model.facemodel_set.all(), form.cleaned_data).save_recognized_face()
        self.success_url = self._image_model.get_absolute_url()
        messages.success(self.request, 'The post has been created!')
        return super(CreateImagePostView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Oops! Something went wrong. Check your inputs!')
        return super(CreateImagePostView, self).form_invalid(form)


class ImagePostDetailView(DetailView):
    template_name = 'image/image_post_detail.html'
    model = ImageModel

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        return get_object_or_404(self.model, slug=slug, status=self.model.PUBLISHED)


class ImagePostEditView(UpdateView):
    form_class = CreateImagePostForm
    template_name = 'image/image_post_create.html'
    model = ImageModel
    initial = {}

    def __init__(self):
        super(ImagePostEditView, self).__init__()

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        object_to_update = get_object_or_404(self.model, slug=slug, status=self.model.PUBLISHED)
        self.initial = {
            'faces': object_to_update.facemodel_set.all(),
            'latitude': object_to_update.latitude,
            'longitude': object_to_update.longitude,
        }
        return object_to_update

    def post(self, request, *args, **kwargs):
        if 'cancel' in request.POST:
            return redirect(self.get_object().get_absolute_url())
        elif 'upload' in request.POST:
            return super(ImagePostEditView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        CreatePeople(self.object.facemodel_set.all(), form.cleaned_data).save_recognized_face()
        messages.success(self.request, 'The post has been updated!')
        return super(ImagePostEditView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Oops! Something went wrong. Check your inputs!')
        return super(ImagePostEditView, self).form_invalid(form)


class ImagePostDeleteView(DeleteView):
    template_name = 'image/image_post_delete.html'
    model = ImageModel

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        return get_object_or_404(self.model, slug=slug, status=self.model.PUBLISHED)

    def get_success_url(self):
        return reverse('image:image-post-list')

    def post(self, request, *args, **kwargs):
        messages.success(self.request, 'The post has been deleted!')
        return super(ImagePostDeleteView, self).post(request, *args, **kwargs)


class ImagePostListView(ListView):
    queryset = ImageModel.objects.filter(status=ImageModel.PUBLISHED)
    paginate_by = 100
