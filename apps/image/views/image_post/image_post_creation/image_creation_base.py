"""
This module contains ImageCreationBase base class for image post creation inherited
by ImagePostCreate and ImagePostUpload classes.
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView

from apps.image.models.image_model import ImageModel


class ImageCreationBase(LoginRequiredMixin, FormView):
    """Represents image post creation base class."""

    def get_draft_if_exists(self):
        """If exists returns user's ImageModel QuerySet with status DRAFT."""
        return ImageModel.objects.filter(user=self.request.user, status=ImageModel.DRAFT)
