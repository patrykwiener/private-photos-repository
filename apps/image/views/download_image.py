import mimetypes
import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View

from apps.image.models.image_model import ImageModel


class ImageDownload(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        image = get_object_or_404(ImageModel, slug=kwargs['slug'], user=request.user)
        content_type = mimetypes.guess_type(image.image.name)[0]
        with open(image.image.path, 'rb') as file:
            response = HttpResponse(file.read(), content_type=content_type)
            response['Content-Length'] = os.path.getsize(image.image.path)
            image_name = image.image.name.split('/')[-1]
            response['Content-Disposition'] = 'attachment; filename={}'.format(image_name)
            return response
