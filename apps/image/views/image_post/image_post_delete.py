from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from apps.image.models.image_model import ImageModel


class ImagePostDelete(LoginRequiredMixin, DeleteView):
    template_name = 'image/image_post_delete.html'
    model = ImageModel
    success_url = reverse_lazy('image:image-post-list')

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        return get_object_or_404(self.model, user=self.request.user, slug=slug, status=self.model.PUBLISHED)

    def post(self, request, *args, **kwargs):
        messages.success(self.request, 'The image has been deleted!')
        return super(ImagePostDelete, self).post(request, *args, **kwargs)
