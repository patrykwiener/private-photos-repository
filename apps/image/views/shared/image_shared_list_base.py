import abc

from apps.image.views.image_post_list_base import ImagePostListBase


class ImageSharedListBase(ImagePostListBase, metaclass=abc.ABCMeta):

    def __init__(self):
        super().__init__()
        self.shared_images = {}

    def get(self, request, *args, **kwargs):
        super_get_result = super().get(request, *args, **kwargs)

        self.create_shared_images()

        return super_get_result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shared_images'] = self.shared_images
        return context

    @abc.abstractmethod
    def create_shared_images(self):
        pass
