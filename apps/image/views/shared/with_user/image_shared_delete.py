"""
This module contains ImageSharedDelete class view responsible for deletion of the shared with
user image posts.
"""
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from apps.image.views.shared.image_shared_delete_base import ImageSharedDeleteBase


class ImageSharedDelete(ImageSharedDeleteBase):
    """Represents deletion of the shared with user image posts view."""
    template_name = 'image/shared_image_delete.html'
    success_url = reverse_lazy('image:shared')

    def get_object(self, queryset=None):
        """Returns SharedImageModel object to delete found by URL image slug."""
        return get_object_or_404(self.model, image__slug=self.slug,
                                 recipient=self.request.user)
