from apps.image.models.image_model import ImageModel
from apps.image.views.shared.image_shared_list_base import ImageSharedListBase


class ImageSharedByUserList(ImageSharedListBase):
    template_name = 'image/shared_by_user_image_list.html'

    def create_shared_images(self):
        for image in self.queryset.distinct():
            for shared_image in image.sharedimagemodel_set.all():
                self.shared_images.setdefault(shared_image.recipient, []).append(image)

    def get(self, request, *args, **kwargs):
        self.queryset = ImageModel.published.filter(sharedimagemodel__image__user=self.request.user)

        return super().get(request, *args, **kwargs)


