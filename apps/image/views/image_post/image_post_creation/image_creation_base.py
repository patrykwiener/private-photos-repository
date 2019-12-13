from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView

from apps.image.models.image_model import ImageModel


class ImageCreationBase(LoginRequiredMixin, FormView):
    def __init__(self):
        super(ImageCreationBase, self).__init__()

    def get_draft_if_exists(self):
        return ImageModel.objects.filter(user=self.request.user, status=ImageModel.DRAFT)
