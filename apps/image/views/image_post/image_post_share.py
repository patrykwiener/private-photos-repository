from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView

from apps.image.forms.image_post_share_form import ImagePostShareForm
from apps.image.models.image_model import ImageModel
from apps.image.models.shared_image_model import SharedImageModel
from apps.users.models import CustomUser


class ImagePostShare(LoginRequiredMixin, FormView):
    form_class = ImagePostShareForm
    template_name = 'image/image_share.html'
    success_url = reverse_lazy('image:image-post-list')

    @property
    def image(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(ImageModel, user=self.request.user, slug=slug, status=ImageModel.PUBLISHED)

    def get(self, request, *args, **kwargs):
        self.extra_context = {
            'object': self.image,
        }
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.extra_context = {
            'object': self.image,
        }
        self.initial = {
            'user': self.request.user,
            'image': self.image
        }
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        SharedImageModel.objects.create(
            recipient=CustomUser.objects.get(email=form.cleaned_data['email']),
            image=self.image,
        )
        messages.success(self.request, "You have shared the post with {}!".format(form.cleaned_data['email']))
        return super().form_valid(form)
