"""
This module contains ImageSharedListBase base class view responsible for displaying image shared
lists.
"""
import abc
from typing import Dict, List

from apps.image.models import ImageModel
from apps.image.views.image_post_list_base import ImagePostListBase
from apps.users.models import CustomUser


class ImageSharedListBase(ImagePostListBase, metaclass=abc.ABCMeta):
    """Base class for shared image list views."""

    def __init__(self):
        super().__init__()
        self.shared_images = {}  # type: Dict[CustomUser, List[ImageModel]]

    def get(self, request, *args, **kwargs):
        """Handles GET request. Creates shared images dict."""
        get_response = super().get(request, *args, **kwargs)
        self.create_shared_images()
        return get_response

    def get_context_data(self, **kwargs):
        """Returns view standard context with added shared_images attr."""
        context = super().get_context_data(**kwargs)
        context['shared_images'] = self.shared_images
        return context

    @abc.abstractmethod
    def create_shared_images(self):
        """Assigns shared_images attr."""
