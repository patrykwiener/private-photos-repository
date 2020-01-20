"""
This module contains ImageSharedDeleteBase base class view responsible for image posts sharing
deletion.
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DeleteView

from apps.image.models.shared_image_model import SharedImageModel


class ImageSharedDeleteBase(LoginRequiredMixin, DeleteView):
    """Base class for image post sharing deletion."""
    model = SharedImageModel

    def __init__(self):
        super().__init__()
        self.slug = None

    def setup(self, request, *args, **kwargs):
        """Initializes attributes."""
        super().setup(request, *args, **kwargs)
        self.slug = self.kwargs.get('slug')
