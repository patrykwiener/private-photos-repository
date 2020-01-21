"""This module contains ImagePostList class view responsible for all image post displaying."""
from apps.image.models.image_model import ImageModel
from apps.image.views.image_post_list_base import ImagePostListBase


class ImagePostList(ImagePostListBase):
    """Represents all image posts view."""
    template_name = 'image/image_list.html'

    def get(self, request, *args, **kwargs):
        """Returns user's all image posts."""
        self.queryset = ImageModel.published.filter(user=self.request.user)
        return super().get(request, *args, **kwargs)
