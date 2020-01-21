"""This module contains ImagePostDetail class view responsible for image post detail view."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from apps.image.models.image_model import ImageModel


class ImagePostDetail(LoginRequiredMixin, DetailView):
    """Represents image post detail view."""
    template_name = 'image/image_post_detail.html'
    model = ImageModel

    def get_object(self, queryset=None):
        """Returns ImageModel object to display its details found by URL slug."""
        slug = self.kwargs.get('slug')
        return get_object_or_404(self.model, user=self.request.user, slug=slug,
                                 status=self.model.PUBLISHED)
