from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from apps.image.models.image_model import ImageModel
from apps.image.views.shared.image_shared_delete_base import ImageSharedDeleteBase


class ImageSharedDelete(ImageSharedDeleteBase):
    template_name = 'image/shared_image_delete.html'
    success_url = reverse_lazy('image:shared')

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, image__slug=self.slug,
                                 recipient=self.request.user)
