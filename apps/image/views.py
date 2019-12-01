from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView, UpdateView, DeleteView, CreateView
from taggit.models import Tag

from apps.image.forms import ImageUploadForm, CreateImagePostForm, ShareImageForm
from apps.image.models.image_model import ImageModel
from apps.image.models.recognized_person_model import RecognizedPersonModel
from apps.image.models.shared_image_model import SharedImageModel
from apps.image.services.create_image_post import CreateImagePost
from apps.image.services.create_people import CreatePeople
from apps.image.services.image_processing.recognition import Recognition
from apps.image.services.upload_image import UploadImage
from apps.users.models import CustomUser


class UploadImageBase(LoginRequiredMixin, FormView):
    def __init__(self):
        super(UploadImageBase, self).__init__()

    def get_draft_if_exists(self):
        return ImageModel.objects.filter(user=self.request.user, status=ImageModel.DRAFT)


class UploadImageView(UploadImageBase):
    form_class = ImageUploadForm
    template_name = 'image/image_upload.html'
    success_url = reverse_lazy('image:image-post-create')

    def dispatch(self, request, *args, **kwargs):
        dispatch_result = super(UploadImageView, self).dispatch(request, *args, **kwargs)
        if self.get_draft_if_exists():
            return redirect(self.get_success_url())
        return dispatch_result

    def form_valid(self, form):
        data = form.cleaned_data
        image_model = UploadImage(self.request.user, data).create_draft()
        Recognition(image_model).execute()
        return super(UploadImageView, self).form_valid(form)


class CreateImagePostView(UploadImageBase):
    form_class = CreateImagePostForm
    template_name = 'image/image_post_create.html'
    success_url = reverse_lazy('image:image-post-list')
    upload_url = reverse_lazy("image:image-upload")

    def __init__(self):
        super(CreateImagePostView, self).__init__()
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

    def dispatch(self, request, *args, **kwargs):
        self.obtain_context_attrs()
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
        return super(CreateImagePostView, self).form_valid(form)

    def form_invalid(self, form):
        return super(CreateImagePostView, self).form_invalid(form)


class ImagePostDetailView(DetailView):
    template_name = 'image/image_post_detail.html'
    model = ImageModel

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        return get_object_or_404(self.model, user=self.request.user, slug=slug, status=self.model.PUBLISHED)


class ImagePostEditView(LoginRequiredMixin, UpdateView):
    form_class = CreateImagePostForm
    template_name = 'image/image_post_create.html'
    model = ImageModel
    initial = {}

    def __init__(self):
        super(ImagePostEditView, self).__init__()

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        object_to_update = get_object_or_404(self.model, user=self.request.user, slug=slug, status=self.model.PUBLISHED)
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
        return super(ImagePostEditView, self).form_invalid(form)


class ImagePostDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'image/image_post_delete.html'
    model = ImageModel
    success_url = reverse_lazy('image:image-post-list')

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        return get_object_or_404(self.model, user=self.request.user, slug=slug, status=self.model.PUBLISHED)

    def post(self, request, *args, **kwargs):
        messages.success(self.request, 'The image has been deleted!')
        return super(ImagePostDeleteView, self).post(request, *args, **kwargs)


class ImagePostListView(LoginRequiredMixin, ListView):
    paginate_by = 100
    template_name = 'image/image_list.html'
    tag = None
    person = None

    def get(self, request, *args, **kwargs):
        self.queryset = ImageModel.published.filter(user=self.request.user)
        tag_slug = 'tag_slug'
        if tag_slug in kwargs:
            self.tag = get_object_or_404(Tag, slug=kwargs[tag_slug])
            self.queryset = self.queryset.filter(tags__in=[self.tag])
        person_slug = 'person_slug'
        if person_slug in kwargs:
            self.person = get_object_or_404(RecognizedPersonModel, slug=kwargs[person_slug])
            self.queryset = self.queryset.filter(facemodel__person__in=[self.person])
        return super(ImagePostListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ImagePostListView, self).get_context_data(**kwargs)
        context['tag'] = self.tag
        context['person'] = self.person
        return context


class SharedImageListView(LoginRequiredMixin, ListView):
    paginate_by = 100
    template_name = 'image/shared_image_list.html'
    tag = None
    person = None

    def get(self, request, *args, **kwargs):
        self.queryset = ImageModel.objects.filter(sharedimagemodel__recipient=self.request.user)
        tag_slug = 'tag_slug'
        if tag_slug in kwargs:
            self.tag = get_object_or_404(Tag, slug=kwargs[tag_slug])
            self.queryset = self.queryset.filter(tags__in=[self.tag])
        person_slug = 'person_slug'
        if person_slug in kwargs:
            self.person = get_object_or_404(RecognizedPersonModel, slug=kwargs[person_slug])
            self.queryset = self.queryset.filter(facemodel__person__in=[self.person])
        return super(SharedImageListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SharedImageListView, self).get_context_data(**kwargs)
        context['tag'] = self.tag
        context['person'] = self.person
        return context


class SharedImageDetail(LoginRequiredMixin, DetailView):
    template_name = 'image/shared_image_detail.html'
    model = ImageModel

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        return get_object_or_404(self.model, sharedimagemodel__recipient=self.request.user, slug=slug,
                                 status=self.model.PUBLISHED)


class ShareImageCreateView(LoginRequiredMixin, FormView):
    form_class = ShareImageForm
    template_name = 'image/image_share.html'
    success_url = reverse_lazy('image:image-post-list')

    @property
    def image(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(ImageModel, user=self.request.user, slug=slug, status=ImageModel.PUBLISHED)

    def dispatch(self, request, *args, **kwargs):
        self.extra_context = {
            'object': self.image,
        }
        return super(ShareImageCreateView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.initial = {
            'user': self.request.user,
            'image': self.image
        }
        return super(ShareImageCreateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        SharedImageModel.objects.create(
            recipient=CustomUser.objects.get(email=form.cleaned_data['email']),
            image=self.image,
        )
        messages.success(self.request, "You have shared the post!")
        return super(ShareImageCreateView, self).form_valid(form)
