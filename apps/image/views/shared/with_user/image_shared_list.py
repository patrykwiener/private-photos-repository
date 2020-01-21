"""
This module contains ImageSharedList class view displaying all shared with user image posts.
"""
from apps.image.models.image_model import ImageModel
from apps.image.views.shared.image_shared_list_base import ImageSharedListBase


class ImageSharedList(ImageSharedListBase):
    """View class displaying all shared with user image posts."""
    template_name = 'image/shared_image_list.html'

    def create_shared_images(self):
        """
        Assigns shared_image attr with a dict of shared images users as keys and lists of shared
        image posts as values. That means the attr should be of type:
                                Dict[CustomUser, List[ImageModel]]
        """
        for image in self.queryset.distinct():
            for shared_image in image.sharedimagemodel_set.filter(recipient=self.request.user):
                self.shared_images.setdefault(shared_image.image.user, []).append(image)

    def get(self, request, *args, **kwargs):
        """Handles GET request. Sets queryset attr with all shared with user image posts."""
        self.queryset = ImageModel.published.filter(sharedimagemodel__recipient=self.request.user)
        return super().get(request, *args, **kwargs)
