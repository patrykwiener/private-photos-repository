from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from apps.image.models.image_model import ImageModel


class ImageSharedDetail(LoginRequiredMixin, DetailView):
    template_name = 'image/shared_image_detail.html'
    model = ImageModel

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        return get_object_or_404(self.model, sharedimagemodel__recipient=self.request.user, slug=slug,
                                 status=self.model.PUBLISHED)
