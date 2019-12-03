from apps.image.models.image_model import ImageModel
from apps.image.views.shared.image_shared_list_base import ImageSharedListBase


class ImageSharedList(ImageSharedListBase):
    template_name = 'image/shared_image_list.html'

    def create_shared_images(self):
        for image in self.queryset.distinct():
            for shared_image in image.sharedimagemodel_set.all():
                self.shared_images.setdefault(shared_image.image.user, []).append(image)

    def get(self, request, *args, **kwargs):
        self.queryset = ImageModel.published.filter(sharedimagemodel__recipient=self.request.user)

        return super(ImageSharedList, self).get(request, *args, **kwargs)
