"""This module contains ImagePostDelete class view responsible for image post delete."""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from apps.image.models.image_model import ImageModel


class ImagePostDelete(LoginRequiredMixin, DeleteView):
    """Represents image post delete view."""
    template_name = 'image/image_post_delete.html'
    model = ImageModel
    success_url = reverse_lazy('image:image-post-list')

    def get_object(self, queryset=None):
        """Returns ImageModel object to delete found by URL slug."""
        slug = self.kwargs.get('slug')
        return get_object_or_404(self.model, user=self.request.user, slug=slug,
                                 status=self.model.PUBLISHED)

    def post(self, request, *args, **kwargs):
        """Adds messages about image deletion."""
        messages.success(self.request, 'The image has been deleted!')
        return super().post(request, *args, **kwargs)
