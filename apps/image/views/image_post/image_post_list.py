from apps.image.models.image_model import ImageModel
from apps.image.views.image_post_list_base import ImagePostListBase


class ImagePostList(ImagePostListBase):
    template_name = 'image/image_list.html'

    def get(self, request, *args, **kwargs):
        self.queryset = ImageModel.published.filter(user=self.request.user)

        return super().get(request, *args, **kwargs)

