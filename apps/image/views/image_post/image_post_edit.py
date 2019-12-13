from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import UpdateView

from apps.image.forms.image_post_create_form import ImagePostCreateForm
from apps.image.models.image_model import ImageModel
from apps.image.services.recognized_people_service import RecognizedPeopleService


class ImagePostEdit(LoginRequiredMixin, UpdateView):
    form_class = ImagePostCreateForm
    template_name = 'image/image_post_create.html'
    model = ImageModel

    def __init__(self):
        super(ImagePostEdit, self).__init__()

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
            return super(ImagePostEdit, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        RecognizedPeopleService(self.object.facemodel_set.all(), form.cleaned_data).save_recognized_face()
        messages.success(self.request, 'The post has been updated!')
        return super(ImagePostEdit, self).form_valid(form)