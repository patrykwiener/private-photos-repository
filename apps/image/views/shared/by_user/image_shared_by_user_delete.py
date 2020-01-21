"""
This module contains ImageSharedByUserDelete class view responsible for share canceling of the
shared by user image posts.
"""
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from apps.image.views.shared.image_shared_delete_base import ImageSharedDeleteBase
from apps.users.models import CustomUser


class ImageSharedByUserDelete(ImageSharedDeleteBase):
    """Represents share canceling of the shared by user image posts."""
    template_name = 'image/shared_by_user_image_delete.html'
    success_url = reverse_lazy('image:shared-by-user')

    def get_object(self, queryset=None):
        """Returns SharedImageModel object to delete found by URL image slug."""
        recipient = get_object_or_404(
            CustomUser,
            id=self.kwargs.get('recipient_id')
        )
        return get_object_or_404(
            self.model,
            image__user=self.request.user,
            image__slug=self.slug,
            recipient=recipient
        )
